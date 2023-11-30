/*global describe, context, beforeEach, it*/

const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("Collateral", function () {
    let collateral;
    let agentRegistry;
    let signers;
    let deployer;
    const agentHash = "0x" + "5".repeat(64);
    const AddressZero = ethers.constants.AddressZero;

    beforeEach(async function () {
        const Collateral = await ethers.getContractFactory("Collateral");
        collateral = await Collateral.deploy(AddressZero, AddressZero, AddressZero, AddressZero, AddressZero,
            AddressZero, AddressZero, AddressZero, AddressZero, AddressZero);
        await collateral.deployed();

        signers = await ethers.getSigners();
        deployer = signers[0];
    });

    context("Initialization", async function () {
        it("Checking for arguments passed to the constructor", async function () {
        });
    });
});
