// SPDX-License-Identifier: MIT
pragma solidity ^0.8.21;

import {ERC721TokenReceiver} from "../lib/solmate/src/tokens/ERC721.sol";

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
/// @param registry Registry contract address.
/// @param unitId Unit Id.
error OperatorOnly(address sender, address operator, address registry, uint256 unitId);

error WrongAssetStatus(address registry, uint256 unitId, AssetStatus status);

/// @title Collateral - Smart contract for managing registry collaterals
contract Collateral is ERC721TokenReceiver {
    event OperatorUpdated(address operator);
    event Applied(address indexed borrower, address indexed registry, uint256 unitId);
    event Collateralised(address indexed borrower, address indexed registry, uint256 unitId);
    event Owned(address indexed borrower, address indexed registry, uint256 unitId);
    event Unset(address indexed borrower, address indexed registry, uint256 unitId);

    // Version number
    string public constant VERSION = "1.0.0";
    // Contract owner
    address public owner;
    // Agent operator multisig address
    address public operator;
    // Map of keccak256(borrower address, registry contract address, unit Id) => status
    mapping(bytes32 => AssetStatus) public mapBorrowerHashStatuses;

    /// @dev Collateral constructor.
    /// @param _operator Agent operator multisig address.
    constructor(address _operator) {
        operator = _operator;
        owner = msg.sender;
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
            revert OperatorOnly(msg.sender, operator, registry, unitId);
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

    function setCollateralised(address borrower, address registry, uint256 unitId) external {
        _setStatus(borrower, registry, unitId, AssetStatus.Collateralised, AssetStatus.Applied);

        emit Collateralised(borrower, registry, unitId);
    }

    function setOwned(address borrower, address registry, uint256 unitId) external {
        _setStatus(borrower, registry, unitId, AssetStatus.Owned, AssetStatus.Collateralised);

        emit Owned(borrower, registry, unitId);
    }

    function setUnset(address borrower, address registry, uint256 unitId) external {
        // Check the function access
        if (msg.sender != operator) {
            revert OperatorOnly(msg.sender, operator, registry, unitId);
        }

        bytes32 borrowerHash = keccak256(abi.encode(borrower, registry, unitId));
        AssetStatus status = mapBorrowerHashStatuses[borrowerHash];
        if (status == AssetStatus.Owned) {
            revert WrongAssetStatus(registry, unitId, status);
        }

        mapBorrowerHashStatuses[borrowerHash] = AssetStatus.Unset;

        emit Unset(borrower, registry, unitId);
    }
}