// SPDX-License-Identifier: MIT
pragma solidity ^0.8.21;

import {ERC721TokenReceiver} from "../lib/solmate/src/tokens/ERC721.sol";
import {IERC20} from "./interfaces/IERC20.sol";

interface IDispenser {
    /// @dev Claims incentives for the owner of components / agents.
    /// @notice `msg.sender` must be the owner of components / agents they are passing, otherwise the function will revert.
    /// @notice If not all `unitIds` belonging to `msg.sender` were provided, they will be untouched and keep accumulating.
    /// @param unitTypes Set of unit types (component / agent).
    /// @param unitIds Set of corresponding unit Ids where account is the owner.
    /// @return reward Reward amount in ETH.
    /// @return topUp Top-up amount in OLAS.
    function claimOwnerIncentives(uint256[] memory unitTypes, uint256[] memory unitIds) external
        returns (uint256 reward, uint256 topUp);
}

// Service Registry interface
interface IServiceRegistry {
    /// @dev Gets the service instance from the map of services.
    /// @param serviceId Service Id.
    /// @return securityDeposit Registration activation deposit.
    /// @return multisig Service multisig address.
    /// @return configHash IPFS hashes pointing to the config metadata.
    /// @return threshold Agent instance signers threshold.
    /// @return maxNumAgentInstances Total number of agent instances.
    /// @return numAgentInstances Actual number of agent instances.
    /// @return state Service state.
    function mapServices(uint256 serviceId) external view returns (
        uint96 securityDeposit,
        address multisig,
        bytes32 configHash,
        uint32 threshold,
        uint32 maxNumAgentInstances,
        uint32 numAgentInstances,
        uint8 state
    );
}

interface IServiceManager {
    /// @dev Terminates the service.
    /// @param serviceId Service Id.
    /// @return success True, if function executed successfully.
    /// @return refund Refund for the service owner.
    function terminate(uint256 serviceId) external returns (bool success, uint256 refund);
}

interface IAave {
    /// @dev deposits The underlying asset into the reserve. A corresponding amount of the overlying asset (aTokens)
    /// is minted.
    /// @param asset the address of the reserve
    /// @param amount the amount to be deposited
    /// @param onBehalfOf the address for which msg.sender is depositing.
    /// @param referralCode integrators are assigned a referral code and can potentially receive rewards.
    function deposit(address asset, uint256 amount, address onBehalfOf, uint16 referralCode) external payable;

    /// @dev Allows users to borrow a specific amount of the reserve currency, provided that the borrower
    ///      already deposited enough collateral.
    /// @param reserve the address of the reserve
    /// @param amount the amount to be borrowed
    /// @param interestRateMode the interest rate mode at which the user wants to borrow. Can be 0 (STABLE) or 1 (VARIABLE)
    /// @param referralCode integrators are assigned a referral code and can potentially receive rewards.
    /// @param onBehalfOf the address for which msg.sender is borrowing.
    function borrow(
        address reserve,
        uint256 amount,
        uint256 interestRateMode,
        uint16 referralCode,
        address onBehalfOf
    ) external;

    /// @notice Repays a borrow on the specific reserve, for the specified amount (or for the whole amount, if type(uint256).max is specified).
    /// @param asset the address of the reserve on which the user borrowed
    /// @param amount the amount to repay, or type(uint256).max if the user wants to repay everything
    /// @param interestRateMode the interest rate mode at which the user wants to borrow. Can be 0 (STABLE) or 1 (VARIABLE)
    /// @param onBehalfOf the address for which msg.sender is repaying.
    function repay(
        address asset,
        uint256 amount,
        uint256 interestRateMode,
        address onBehalfOf
    ) external returns (uint256);
}

interface IClipperRouter {
    function clipperSwap(address srcToken, address dstToken, uint256 amount, uint256 minReturn)
        external returns (uint256 returnAmount);
}

interface IWETH {
    function deposit() external payable;
    function withdraw(uint256 amount) external;
}

enum AssetStatus {
    LoanClosed,
    QuoteProvided,
    LoanTermsAccepted,
    Liquidated
}

/// @dev Only `owner` has a privilege, but the `sender` was provided.
/// @param sender Sender address.
/// @param owner Required grower address.
error OwnerOnly(address sender, address owner);

/// @dev Provided zero address.
error ZeroAddress();

/// @dev Only `operator` has a privilege, but the `sender` was provided.
/// @param sender Sender address.
/// @param operator Required operator address.
error OperatorOnly(address sender, address operator);

/// @dev Wrong asset status.
/// @param registry Registry contract address.
/// @param unitId Unit Id.
/// @param status Asset status.
error WrongAssetStatus(address registry, uint256 unitId, AssetStatus status);

/// @dev Insufficient contract balance.
/// @param required Required balance.
/// @param available Available balance.
error InsufficientBalance(uint256 required, uint256 available);

/// @dev Failure of a transfer.
/// @param token Address of a token.
/// @param from Address `from`.
/// @param to Address `to`.
/// @param amount Token amount.
error TransferFailed(address token, address from, address to, uint256 amount);

/// @dev Wrong service state.
/// @param serviceId Service Id.
/// @param state Service state.
error WrongServiceState(uint256 serviceId, uint8 state);

/// @dev Service multisig call failed.
/// @param multisig Service multisig address.
/// @param data Payload data.
error MultisigCallFailed(address multisig, bytes data);

/// @dev Deposit low then threshold
error LowDeposit(uint256 amount, uint256 min_amount);

/// @title Collateral - Smart contract for managing registry collaterals
contract Collateral is ERC721TokenReceiver {
    event Deposit(address indexed sender, uint256 value);
    event TokenDeposit(address indexed sender, address indexed token, uint256 value);
    event OperatorUpdated(address indexed operator);
    event QuoteProvided(address indexed borrower, address indexed registry, uint256 unitId);
    event LoanTermsAccepted(address indexed borrower, address indexed registry, uint256 unitId);
    event Liquidated(address indexed borrower, address indexed registry, uint256 unitId);
    event LoanClosed(address indexed borrower, address indexed registry, uint256 unitId);

    // Version number
    string public constant VERSION = "1.0.0";
    // Default borrower fee
    uint256 public constant DEFAULT_BORROWER_FEE = 1 ether;
    // Default depositor fee
    uint256 public constant DEFAULT_DEPOSITOR_FEE = 1;
    // Min deposit
    uint256 public constant MIN_DEPOSIT = 1 ether;
    // ETH address
    address public constant ETH_TOKEN_ADDRESS = 0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE;
    // Value for the contract signature validation: bytes4(keccak256("isValidSignature(bytes32,bytes)")
    bytes4 constant internal MAGIC_VALUE = 0x1626ba7e;

    // Component registry address
    address public immutable componentRegistry;
    // Agent registry address
    address public immutable agentRegistry;
    // Service registry address
    address public immutable serviceRegistry;
    // Aave pool address
    address public immutable aavePool;
    // Clipper router address
    address public immutable clipperRouter;
    // DAI address
    address public immutable dai;
    // DAI address
    address public immutable weth;

    // Service manager address
    address public serviceManager;
    // Dispenser address
    address public dispenser;
    // Contract owner
    address public owner;
    // Agent operator multisig address
    address public operator;
    // Debt balance
    uint256 public debt;
    // Map of depositor balances
    mapping (address => uint256) public mapDepositorBalances;
    // Map of keccak256(borrower address, registry contract address, unit Id) => status
    mapping (bytes32 => AssetStatus) public mapBorrowerHashStatuses;
    // Map of verified offer hashes
    mapping (bytes32 => bool) public mapVerifiedHashes;

    /// @dev Collateral constructor.
    /// @param _operator Agent operator multisig address.
    constructor(
        address _operator,
        address _componentRegistry,
        address _agentRegistry,
        address _serviceRegistry,
        address _serviceManager,
        address _dispenser,
        address _aavePool,
        address _clipperRouter,
        address _dai,
        address _weth
    )
    {
        operator = _operator;
        componentRegistry = _componentRegistry;
        agentRegistry = _agentRegistry;
        serviceRegistry = _serviceRegistry;

        // TODO: service manager and dispenser might change, add a setter for them
        serviceManager = _serviceManager;
        dispenser = _dispenser;

        aavePool = _aavePool;
        clipperRouter = _clipperRouter;
        dai = _dai;
        weth = _weth;
        owner = msg.sender;
    }

    receive() external payable {
        if(msg.value < MIN_DEPOSIT) {
            revert LowDeposit(msg.value, MIN_DEPOSIT);
        }
        uint256 fee = (msg.value * DEFAULT_DEPOSITOR_FEE) / 100;
        uint256 adjustedDeposit = msg.value + fee;
        mapDepositorBalances[msg.sender] += adjustedDeposit;
        debt += adjustedDeposit;

        emit Deposit(msg.sender, msg.value);
    }

    function deposit(address token, uint256 amount) external payable {
        IERC20(token).transferFrom(msg.sender, address(this), amount);

        // Exchange into WETH via 1inch
        IERC20(token).approve(clipperRouter, amount);
        uint256 amountETH = IClipperRouter(clipperRouter).clipperSwap(token, weth, amount, 0);
        if(amountETH < MIN_DEPOSIT) {
            revert LowDeposit(amountETH, MIN_DEPOSIT);
        }

        // Record the depositor value and fee in ETH
        uint256 fee = (amountETH * DEFAULT_DEPOSITOR_FEE) / 100;
        uint256 adjustedDeposit = amountETH + fee;
        mapDepositorBalances[msg.sender] += adjustedDeposit;
        debt += adjustedDeposit;

        emit TokenDeposit(msg.sender, token, amount);
    }

    /// @dev Sets the agent operator multisig address.
    /// @param _operator Agent operator address.
    function setOperator(address _operator) external {
        // Check the contract ownership
        if (msg.sender != owner) {
            revert OwnerOnly(msg.sender, owner);
        }

        if (_operator == address(0)) {
            revert ZeroAddress();
        }

        operator = _operator;
    }

    function _setStatus(
        address borrower,
        address registry,
        uint256 unitId,
        AssetStatus actual,
        AssetStatus previous
    ) internal
    {
        // Check the function access
        if (msg.sender != operator) {
            revert OperatorOnly(msg.sender, operator);
        }

        bytes32 borrowerHash = keccak256(abi.encode(borrower, registry, unitId));
        AssetStatus status = mapBorrowerHashStatuses[borrowerHash];
        if (status != previous) {
            revert WrongAssetStatus(registry, unitId, status);
        }

        mapBorrowerHashStatuses[borrowerHash] = actual;
    }

    function setQuoteProvided(
        address borrower,
        address registry,
        uint256 unitId,
        uint256 unitPrice,
        bytes32 offerHash
    ) external
    {
        mapVerifiedHashes[offerHash] = true;

        _setStatus(borrower, registry, unitId, AssetStatus.QuoteProvided, AssetStatus.LoanClosed);

        // Approve DAI for the borrower (to be transferred by the PWN Vault)
        IERC20(dai).approve(borrower, unitPrice);

        emit QuoteProvided(borrower, registry, unitId);
    }

    function setLoanTermsAccepted(
        address borrower,
        address registry,
        uint256 unitId,
        uint256 unitPrice,
        uint256 unitPriceETH
    ) external
    {
        // TODO: Choose between a native token and another ERC20 token to deposit to Aave
        // TODO: Right now we are going to deposit a native token only
        // TODO: account for the slippage between unitPrice and unitPriceETH
        // Overall value in ETH: unit price + borrower fee to return to Aave
        // (+ depositor fee to return to the depositor recorded in the mapDepositorBalances)
        uint256 depositValue = unitPriceETH + DEFAULT_BORROWER_FEE;
        uint256 balance = address(this).balance;
        if (depositValue > balance) {
            revert InsufficientBalance(depositValue, balance);
        }
        // TODO install hook such that portfolio position is hedged using a post tx hook. HERE we just borrow.
        IWETH(weth).deposit{value: unitPriceETH}();
        IERC20(weth).approve(aavePool, unitPriceETH);
        IAave(aavePool).deposit(ETH_TOKEN_ADDRESS, unitPriceETH, address(this), 0);
        IAave(aavePool).borrow(dai, unitPrice, 0, 0, address(this));

        _setStatus(borrower, registry, unitId, AssetStatus.LoanTermsAccepted, AssetStatus.QuoteProvided);

        emit LoanTermsAccepted(borrower, registry, unitId);
    }

    function setLiquidation(address borrower, address registry, uint256 unitId) external {
        // TODO: terminate the service and withdraw all the specified funds from its multisig (info gathered by the operator)
        // TODO: The service is supposed to have a correct termination skill such that after the termination the contract becomes the service multisig owner
        IServiceManager(serviceManager).terminate(unitId);

        // Repay Aave loan as the borrower was not able to repay
        // TODO: calculate the exact amount of DAI for repayment
        IERC20(dai).approve(aavePool, type(uint256).max);
        uint256 paybackAmount = IAave(aavePool).repay(dai, type(uint256).max, 0, address(this));
        IWETH(weth).withdraw(paybackAmount);

        // Update the collateral asset status to Liquidated
        _setStatus(borrower, registry, unitId, AssetStatus.Liquidated, AssetStatus.LoanTermsAccepted);

        emit Liquidated(borrower, registry, unitId);
    }

    function setLoanClosed(address borrower, address registry, uint256 unitId) external {
        // Check the function access
        if (msg.sender != operator) {
            revert OperatorOnly(msg.sender, operator);
        }

        bytes32 borrowerHash = keccak256(abi.encode(borrower, registry, unitId));
        AssetStatus status = mapBorrowerHashStatuses[borrowerHash];
        if (status == AssetStatus.Liquidated) {
            revert WrongAssetStatus(registry, unitId, status);
        }

        if(status == AssetStatus.LoanTermsAccepted) {
            // TODO install hook such that the position of the portfolio is Rehedged using a post tx hook. HERE we just repay.
            // TODO: liquidate the loan in Aave as the borrower was not able to repay
            // Repay Aave loan, if AssetStatus.LoanTermsAccepted -> AssetStatus.LoanClosed
            IERC20(dai).approve(aavePool, type(uint256).max);
            uint256 paybackAmount = IAave(aavePool).repay(dai, type(uint256).max, 0, address(this));
            IWETH(weth).withdraw(paybackAmount);
        }

        mapBorrowerHashStatuses[borrowerHash] = AssetStatus.LoanClosed;

        emit LoanClosed(borrower, registry, unitId);
    }
    
    function liquidateDefaultedPosition(address borrower, address registry, uint256 unitId, bytes memory data) external {
        // Check the function access
        if (msg.sender != operator) {
            revert OperatorOnly(msg.sender, operator);
        }

        bytes32 borrowerHash = keccak256(abi.encode(borrower, registry, unitId));
        AssetStatus status = mapBorrowerHashStatuses[borrowerHash];
        if (status != AssetStatus.Liquidated) {
            revert WrongAssetStatus(registry, unitId, status);
        }

        if (registry == componentRegistry) {
            // TODO: claim rewards and top-ups, if there are any
            // Since this contract is the component owner, it is able to claim its OLAS rewards and top-ups
            uint256[] memory unitTypes = new uint256[](1);
            unitTypes[0] = 0;
            uint256[] memory unitIds = new uint256[](1);
            unitIds[0] = unitId;
            IDispenser(dispenser).claimOwnerIncentives(unitTypes, unitIds);
        } else if (registry == agentRegistry) {
            // Since this contract is the component owner, it is able to claim its OLAS rewards and top-ups
            uint256[] memory unitTypes = new uint256[](1);
            unitTypes[0] = 1;
            uint256[] memory unitIds = new uint256[](1);
            unitIds[0] = unitId;
            IDispenser(dispenser).claimOwnerIncentives(unitTypes, unitIds);
        } else if (registry == serviceRegistry) {
            // TODO: assuming that the service is fully unbonded and this contract is the owner of the service multisig
            // TODO: withdraw funds from the multisig parsing the data, capitalize on any other assets like NFTs
            // Get the service data
            ( , address multisig, , , , , uint8 state) = IServiceRegistry(serviceRegistry).mapServices(unitId);

            // Check the service state (must be unbonded)
            if (state != 1) {
                revert WrongServiceState(unitId, state);
            }

            // Execute the multisig passed data
            (bool success, ) = multisig.call(data);
            if (!success) {
                revert MultisigCallFailed(multisig, data);
            }
        }
        // TODO: sell the unit(s)
    }

    function withdrawToDepositor() external {
        uint256 amount = mapDepositorBalances[msg.sender];
        uint256 balance = address(this).balance;
        if (amount > 0 && balance >= amount) {
            debt -= amount;
            mapDepositorBalances[msg.sender] = 0;
            (bool success, ) = msg.sender.call{value: amount}("");

            if (!success) {
                revert TransferFailed(ETH_TOKEN_ADDRESS, address(this), msg.sender, amount);
            }
        }
    }

    function withdraw(address to) external {
        // Check the contract ownership
        if (msg.sender != owner) {
            revert OwnerOnly(msg.sender, owner);
        }

        uint256 balance = address(this).balance;
        if (balance >= debt) {
            uint256 amount = balance - debt;
            (bool success, ) = to.call{value: amount}("");

            if (!success) {
                revert TransferFailed(ETH_TOKEN_ADDRESS, address(this), msg.sender, amount);
            }
        }
    }

    /// @dev Should return whether the signature provided is valid for the provided hash.
    /// @notice MUST return the bytes4 magic value 0x1626ba7e when function passes.
    /// @param hash Hash of the data to be verified, earlier pre-approved by the multisig operator.
    /// @return magicValue bytes4 magic value.
    function isValidSignature(bytes32 hash, bytes memory) external view returns (bytes4 magicValue) {
        if (mapVerifiedHashes[hash]) {
            magicValue = MAGIC_VALUE;
        }
    }

    function profit() external view returns (int256) {
        return int256(address(this).balance) - int256(debt);
    }

    function getBorrowerHash(address borrower, address registry, uint256 unitId) external pure returns (bytes32) {
        return keccak256(abi.encode(borrower, registry, unitId));
    }

    // TODO: Aave loan health monitoring
}