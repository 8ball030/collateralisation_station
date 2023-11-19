const fs = require("fs");
const globalsFile = "globals.json";
const dataFromJSON = fs.readFileSync(globalsFile, "utf8");
const parsedData = JSON.parse(dataFromJSON);
const operatorAddress = parsedData.operatorAddress;
const serviceRegistryAddress = parsedData.serviceRegistryAddress;
const serviceManagerAddress = parsedData.serviceManagerAddress;
const aavePoolAddress = parsedData.aavePoolAddress;
const clipperRouterAddress = parsedData.clipperRouterAddress;
const daiAddress = parsedData.daiAddress;
const wethAddress = parsedData.wethAddress;
const AddressZero = "0x" + "0".repeat(40);

module.exports = [
    operatorAddress,
    AddressZero,
    AddressZero,
    serviceRegistryAddress,
    serviceManagerAddress,
    AddressZero,
    aavePoolAddress,
    clipperRouterAddress,
    daiAddress,
    wethAddress
];