/*global process*/

const { ethers } = require("hardhat");

async function main() {
    const fs = require("fs");
    const globalsFile = "globals.json";
    const dataFromJSON = fs.readFileSync(globalsFile, "utf8");
    let parsedData = JSON.parse(dataFromJSON);
    const providerName = parsedData.providerName;
    const gasPriceInGwei = parsedData.gasPriceInGwei;
    const operatorAddress = parsedData.operatorAddress;
    const serviceRegistryAddress = parsedData.serviceRegistryAddress;
    const serviceManagerAddress = parsedData.serviceManagerAddress;
    const aavePoolAddress = parsedData.aavePoolAddress;
    const clipperRouterAddress = parsedData.clipperRouterAddress;
    const daiAddress = parsedData.daiAddress;
    const wethAddress = parsedData.wethAddress;
    const AddressZero = ethers.constants.AddressZero;

    let provider;
    if (providerName == "polygon") {
        provider = await ethers.providers.getDefaultProvider("matic");
    } else {
        const mumbaiURL = "https://polygon-mumbai.g.alchemy.com/v2/" + process.env.ALCHEMY_API_KEY_MUMBAI;
        provider = new ethers.providers.JsonRpcProvider(mumbaiURL);
    }
    const signers = await ethers.getSigners();

    const EOA = signers[0];
    // EOA address
    const deployer = await EOA.getAddress();
    console.log("EOA is:", deployer);

    // Transaction signing and execution
    console.log("1. EOA to deploy Collateral contract");
    const Collateral = await ethers.getContractFactory("Collateral");
    console.log("You are signing the following transaction: Collateral.connect(EOA).deploy()");
    const gasPrice = ethers.utils.parseUnits(gasPriceInGwei, "gwei");
    const collateral = await Collateral.connect(EOA).deploy(operatorAddress, AddressZero, AddressZero, serviceRegistryAddress,
        serviceManagerAddress, AddressZero, aavePoolAddress, clipperRouterAddress, daiAddress, wethAddress, { gasPrice });
    const result = await collateral.deployed();

    // Transaction details
    console.log("Contract deployment: Collateral");
    console.log("Contract address:", collateral.address);
    console.log("Transaction:", result.deployTransaction.hash);

    // Wait half a minute for the transaction completion
    await new Promise(r => setTimeout(r, 30000));

    // Writing updated parameters back to the JSON file
    parsedData.collateralAddress = collateral.address;
    fs.writeFileSync(globalsFile, JSON.stringify(parsedData));

    // Contract verification
    if (parsedData.contractVerification) {
        const execSync = require("child_process").execSync;
        execSync("npx hardhat verify --constructor-args scripts/deployment/verify_01_collateral.js --network " + providerName + " " + collateral.address, { encoding: "utf-8" });
    }
}

main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });
