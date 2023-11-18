# Collateralisation Station

Trustless liquidity for your autonomous agent service NFTs.

## Front-end

The [front-end](frontend)


## Smart contracts

The [smart contracts](contracts)


## Multi-agent system

The [multi-agent service](mas)


## Sequence diagram

Collateralisation Station functions at its core by leveraging autonomous agent services, represented as an NFT, as collateral to access liquidity without requiring the sale of the NFT. 
The LoanBotService, an Autonolas multi-agent system, check the amount of claimable OLAS on the service NFT, as well as the current wETH price of OLAS on Uniswap, and the current price of wETH in USD using a Chainlink oracle.
This data is then analyzed and a loan offer is created and forwarded to PWN.
Alice can then assess the offer, and if she accepts to offer, her NFT will be transfered to the PWN smart contract, and she receives her loan from PWN.
She can then either:
1. Repay the loan via PWN, which will subsequently be settled on the LoanAggregatorSmartContract, and her NFT is returned to her.
2. Refuse or fail to repay her loan. Then, a proxy call it made to the multi-agent service owned SAFE multisig, and, as much OLAS as is needed to cover the repayment of Bob + fees, will be liquidated. The LoanBotService transfers these funds to the LoanAggregatorSmartContract, which is used to fullfill the repayment to PWN, at which point ownership of the NFT held in the PWN smart contract will be transfered to LoanAggregatorSmartContract.

Alternatively, or rather what's more, Charlie can donate his OLAS to AAVE to obtain aOLAS and collect fees. The deposited OLAS on AAVE can subsequently be borrowed by the LoanAggregatorSmartContract, and similarly be used to lend out, via PWN, to Alice. The only difference here is that when Alice fails to repay, the LoanBotService liquidates as much as is needed to repay Charlie + fees, via AAVE.


```mermaid
sequenceDiagram 
    participant Bob
    participant LoanAggregatorSmartContract
    participant Alice
    participant PWN
    participant AAVE
    participant LoanBotService
    participant OlasDonationManagerContract
    participant UniswapV2Pools
    participant ChainlinkOracle

    Bob ->> LoanAggregatorSmartContract: Deposit DAI for loans 
    Charlie ->> AAVE: Deposit OLAS for loans 
    AAVE ->> Charlie: aOLAS
    Alice ->> PWN: Loan Request 
    PWN ->> LoanBotService: Poll Loan Requests 
    LoanBotService ->> LoanAggregatorSmartContract: Check Available Funds for loan 
    LoanBotService ->> OlasDonationManagerContract: Check Nft Claimable OLAS 
    LoanBotService ->> UniswapV2Pools: Get OLAS Weth price 
    LoanBotService ->> ChainlinkOracle: Get Weth USD Price 
    LoanBotService ->> LoanBotService: Analyze Data 
    LoanBotService ->> PWN: Create Loan Offer 
    Alice ->> PWN: Accept Offer 
    Alice ->> PWN: TX NFT 

    LoanAggregatorSmartContract ->> AAVE: Borrow OLAS
    AAVE ->> LoanAggregatorSmartContract: OLAS 
    LoanBotService ->> LoanAggregatorSmartContract: TX Loan To fulfill PWN 
    LoanAggregatorSmartContract ->> PWN: OLAS 
    PWN ->> Alice: GIB Loan 
    Alice ->> PWN: Repays Loan 
    PWN ->> LoanAggregatorSmartContract: Settle Loan + Fees
    LoanAggregatorSmartContract ->> Bob: Collect DAI + Fees 
    Alice ->> PWN: REFUSE TO Pay 
    PWN ->>LoanAggregatorSmartContract: txs Alice's nft 
    LoanBotService ->> LoanAggregatorSmartContract: proxy call to multisig
    LoanAggregatorSmartContract ->> OlasDonationManagerContract: claim OLAS 
    LoanBotService ->> LoanAggregatorSmartContract: Liquidate enough to repay Bob (Keeps the rest as OLAS) 
    LoanBotService ->> AAVE: OLAS
    AAVE ->> Charlie: OLAS + fees
    LoanAggregatorSmartContract ->> Bob: Collect DAI + Fees
    LoanAggregatorSmartContract ->> LoanBotServiceService: Collect
```
