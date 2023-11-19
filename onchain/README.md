# Collateralisation Station
## Introduction

This repository contains the Collateralisation Station contracts.

Collateralisation Station harnesses the power of off-chain data manipulation seamlessly connected with the set of
on-chain contracts to govern a decision making in collateralising NFTs representing runnable code, in exchange of a
requested ERC20 token liquidity. The station monitors registry NFTs supplied to the PWN service, estimates their cost
in DAI, and provides a quoted offer to the borrower (being the NFT provider). If the borrower accepts the offer, the
collateralisation service then requests the required DAI supply from the Aave platform in order to pay to the borrower.

If the borrower repays the loan they collateralised their NFT for, the collateralisation service repays DAI to Aave,
earns on fees and provides a payout to the liquidity provider. However, if the borrower defaults on a loan, the NFT gets
owned by the collateralisation contract, still repays DAI to Aave. The service then figures out the best way to liquidate
the NFT position: collect rewards in the form of ERC20 tokens or NFTs, if applicable (assuming the NFT is a service that
has a multisig collecting different assets), or sell the NFT right away.

The service is run on the [Autonolas stack](https://olas.network/).

## Development

### Prerequisites
- This repository follows the standard [`Hardhat`](https://hardhat.org/tutorial/) development process.
- The code is written on Solidity `0.8.21`.
- The standard versions of Node.js along with Yarn are required to proceed further (confirmed to work with Yarn `1.22.19` and npx/npm `10.1.0` and node `v18.17.0`).

### Install the dependencies
The project has submodules to get the dependencies. Make sure you run `git clone --recursive` or init the submodules yourself.
The dependency list is managed by the `package.json` file, and the setup parameters are stored in the `hardhat.config.js` file.
Simply run the following command to install the project:
```
yarn install
```

### Core components
The contracts, deployment scripts and tests are located in the following folders respectively:
```
contracts
scripts
test
```

### Compile the code and run
Compile the code:
```
npx hardhat compile
```
Run the tests:
```
npx hardhat test
```

### Linters
- [`ESLint`](https://eslint.org) is used for JS code.
- [`solhint`](https://github.com/protofire/solhint) is used for Solidity linting.


## Deployment
The deployment of contracts to the test- and main-net is split into step-by-step series of scripts for more control and checkpoint convenience.
The description of deployment procedure can be found here: [deployment](https://github.com/8ball030/collateralisation_station/blob/main/onchain/scripts/deployment).

The contract address on Polygon is located [here](https://polygonscan.com/address/0xeB49bE5DF00F74bd240DE4535DDe6Bc89CEfb994#code).

The finalized contract ABIs for deployment and their number of optimization passes are located here: [ABIs](https://github.com/8ball030/collateralisation_station/blob/main/onchain/abis).


## Acknowledgements
The collateralisation station contracts were inspired and based on the following sources:
- [PWNFinance](https://github.com/PWNFinance/pwn_contracts).
- [Aave](https://github.com/aave/aave-v3-core).
- [1inch](https://docs.1inch.io/docs/aggregation-protocol/smart-contract/ClipperRouter).
- [Rari-Capital](https://github.com/Rari-Capital/solmate).
- [Safe Ecosystem](https://github.com/safe-global/safe-contracts).
- [Valory](https://github.com/valory-xyz/autonolas-registries).
