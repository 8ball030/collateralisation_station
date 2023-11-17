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

interface IServiceManager {
    /// @dev Terminates the service.
    /// @param serviceId Service Id.
    /// @return success True, if function executed successfully.
    /// @return refund Refund for the service owner.
    function terminate(uint256 serviceId) external returns (bool success, uint256 refund);
}

enum AssetStatus {
    Unset,
    Applied,
    Collateralised,
    Owned
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

error WrongAssetStatus(address registry, uint256 unitId, AssetStatus status);

/// @title Collateral - Smart contract for managing registry collaterals
contract Collateral is ERC721TokenReceiver {
    event Deposit(address indexed sender, uint256 value);
    event TokenDeposit(address indexed sender, address indexed token, uint256 value);
    event OperatorUpdated(address indexed operator);
    event Applied(address indexed borrower, address indexed registry, uint256 unitId);
    event Collateralised(address indexed borrower, address indexed registry, uint256 unitId);
    event Owned(address indexed borrower, address indexed registry, uint256 unitId);
    event Unset(address indexed borrower, address indexed registry, uint256 unitId);

    // Version number
    string public constant VERSION = "1.0.0";
    // Component registry address
    address public immutable componentRegistry;
    // Agent registry address
    address public immutable agentRegistry;
    // Service registry address
    address public immutable serviceRegistry;
    // Service manager address
    address public serviceManager;
    // Dispenser address
    address public dispenser;
    // Contract owner
    address public owner;
    // Agent operator multisig address
    address public operator;
    // Map of keccak256(borrower address, registry contract address, unit Id) => status
    mapping(bytes32 => AssetStatus) public mapBorrowerHashStatuses;

    /// @dev Collateral constructor.
    /// @param _operator Agent operator multisig address.
    constructor(
        address _operator,
        address _componentRegistry,
        address _agentRegistry,
        address _serviceRegistry,
        address _serviceManager,
        address _dispenser
    )
    {
        operator = _operator;
        componentRegistry = _componentRegistry;
        agentRegistry = _agentRegistry;
        serviceRegistry = _serviceRegistry;
        // TODO: service manager and dispenser might change, add a setter for them
        serviceManager = _serviceManager;
        dispenser = _dispenser;
        owner = msg.sender;
    }

    receive() external payable {
        emit Deposit(msg.sender, msg.value);
    }

    function deposit(address token, uint256 amount) external payable {
        IERC20(token).transferFrom(msg.sender, address(this), amount);

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

    function setApplied(address borrower, address registry, uint256 unitId) external {
        _setStatus(borrower, registry, unitId, AssetStatus.Applied, AssetStatus.Unset);

        emit Applied(borrower, registry, unitId);
    }

    function setCollateralised(address borrower, address registry, uint256 unitId, uint256 unitPrice) external {
        // TODO: make a loan via Aave

        _setStatus(borrower, registry, unitId, AssetStatus.Collateralised, AssetStatus.Applied);

        emit Collateralised(borrower, registry, unitId);
    }

    function setOwned(address borrower, address registry, uint256 unitId) external {
        // TODO: liquidate the loan in Aave as the borrower was not able to repay

        _setStatus(borrower, registry, unitId, AssetStatus.Owned, AssetStatus.Collateralised);

        emit Owned(borrower, registry, unitId);
    }

    function setUnset(address borrower, address registry, uint256 unitId) external {
        // Check the function access
        if (msg.sender != operator) {
            revert OperatorOnly(msg.sender, operator);
        }

        bytes32 borrowerHash = keccak256(abi.encode(borrower, registry, unitId));
        AssetStatus status = mapBorrowerHashStatuses[borrowerHash];
        if (status == AssetStatus.Owned) {
            revert WrongAssetStatus(registry, unitId, status);
        }

        mapBorrowerHashStatuses[borrowerHash] = AssetStatus.Unset;

        emit Unset(borrower, registry, unitId);
    }
    
    function sellOwnedUnit(address borrower, address registry, uint256 unitId, bytes memory data) external {
        // Check the function access
        if (msg.sender != operator) {
            revert OperatorOnly(msg.sender, operator);
        }

        bytes32 borrowerHash = keccak256(abi.encode(borrower, registry, unitId));
        AssetStatus status = mapBorrowerHashStatuses[borrowerHash];
        if (status != AssetStatus.Owned) {
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
            // TODO: terminate the service and withdraw all the specified funds from its multisig (info gathered by the operator)
            // TODO: The service is supposed to have a correct termination skill such that after the termination the contract becomes the service multisig owner
            IServiceManager(serviceManager).terminate(unitId);
            // TODO: withdraw funds from the multisig parsing the data
        }
        // TODO: sell the unit
    }
    
    // TODO: Aave loan health monitoring
}