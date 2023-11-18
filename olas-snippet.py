import os
import json
import requests
from datetime import datetime, timedelta, timezone
from eth_account.messages import encode_defunct, SignableMessage, encode_structured_data
from eth_keys import keys
import web3
import web3.contract
from web3 import Web3

# change this
WEB_PROVIDER_URL = "https://mainnet.infura.io/v3/a89d9c9e36b44b19be2a812587205eee"
API_BASE_URL = "https://api-staging.pwn.xyz/api/v1/"
OFFER_CONTRACT_ABI_FILE_PATH = "/Users/dev/PycharmProjects/pwn_backend_py/pwn_backend_py/loan/v_1/contract_artefacts/v1.1/PWNSimpleLoanSimpleOffer.json"

# no need to change this inshallah
CHAIN_ID = 1
DAI_CONTRACT_ADDRESS = Web3.to_checksum_address("0x6b175474e89094c44da98b954eedeac495271d0f")
OFFER_CONTRACT_ADDRESS = Web3.to_checksum_address("0x5E551f09b8d1353075A1FF3B484Ee688aCAc02F6")
LOAN_REQUEST_CONTRACT_ADDRESS = Web3.to_checksum_address("0x9Cb87eC6448299aBc326F32d60E191Ef32Ab225D")
LOAN_CONTRACT_ADDRESS = Web3.to_checksum_address("0x50160ff9c19fbE2B5643449e1A321cAc15af2b2C")
TEST_AUTH_WALLET_PRIVATE_KEY = Web3.keccak(os.urandom(4096))

# loan data defaults
LOAN_AMOUNT_WEI = 10**20
LOAN_YIELD_WEI = 10**19
LOAN_DURATION_SECONDS = 30 * 86400
LOAN_VALIDITY_DAYS = 7


def get_contract_class(address):
    with open(OFFER_CONTRACT_ABI_FILE_PATH) as abi_file:
        abi = json.load(abi_file)

    w3 = Web3(Web3.HTTPProvider(WEB_PROVIDER_URL))

    contract = web3.contract.ContractCaller(
        w3=w3,
        abi=abi,
        address=address,
    )
    return contract


def get_auth_nonce(wallet_address):
    response = requests.get(
        f"{API_BASE_URL}web3auth/message_to_sign/{wallet_address}"
    )
    return response.content


def get_loan_requests(
        chain_id,
        loan_request_contract_address: str,
        collateral_address_filter: str | None = None,
):
    url = f"{API_BASE_URL}loan/loan/network/{chain_id}/{loan_request_contract_address}/"
    if collateral_address_filter is not None:
        url = f"{url}?collateral_address={collateral_address_filter}"

    response = requests.get(
        url,
    )
    return response.json()["results"]


def get_next_offer_nonce(chain_id: int, offer_contract_address: str, wallet_address: str):
    # r"nonce/network/(?P<chain_id>\d+)/(?P<contract_address>0x[0-9A-Fa-f]{40})/(?P<wallet_address>0x[0-9A-Fa-f]{40})/$",
    response = requests.get(
        f"{API_BASE_URL}loan/nonce/network/{chain_id}/{offer_contract_address}/{wallet_address}/"
    )
    return response.json()["last_nonce"]+1


def post_loan(
        private_key,
        chain_id,
        offer_contract_address,
        pwn_loan_id,
        api_auth_token,
        loan_asset_contract_address,
        borrower_wallet_address,
        lender_wallet_address,
        loan_asset_amount,
        loan_yield_amount,
        loan_duration_seconds,
        collateral_address,
        collateral_token_id,
        collateral_amount,
        offer_expiration_timestamp,
):
    pk = keys.PrivateKey(private_key)
    wallet_address = pk.public_key.to_checksum_address()

    offer_nonce = get_next_offer_nonce(CHAIN_ID, OFFER_CONTRACT_ADDRESS, wallet_address)

    collateral_category = 1  # always ERC-721 for now

    offer_struct = {
        "collateralCategory": int(collateral_category),  # noqa
        "collateralAddress": collateral_address,
        "collateralId": int(collateral_token_id) if collateral_token_id is not None else 0,
        "collateralAmount": collateral_amount,
        "loanAssetAddress": Web3.to_checksum_address(loan_asset_contract_address),
        "loanAmount": int(loan_asset_amount or 0),
        "loanYield": int(loan_yield_amount or 0),
        "duration": int(loan_duration_seconds or 0),
        "expiration": int(offer_expiration_timestamp or 0),
        "borrower": Web3.to_checksum_address(borrower_wallet_address),
        "lender": Web3.to_checksum_address(wallet_address),
        "isPersistent": False,
        "nonce": int(offer_nonce or 0),
    }

    offer_signable_message = {
        "domain": {
            "chainId": chain_id,
            "verifyingContract": Web3.to_checksum_address(offer_contract_address),
            "name": "PWNSimpleLoanSimpleOffer",
            "version": "1",
        },
        "message": offer_struct,
        "primaryType": "Offer",
        "types": {
            "EIP712Domain": [
                {"name": "name", "type": "string"},
                {"name": "version", "type": "string"},
                {"name": "chainId", "type": "uint256"},
                {"name": "verifyingContract", "type": "address"},
            ],
            "Offer": [
                {"name": "collateralCategory", "type": "uint8"},
                {"name": "collateralAddress", "type": "address"},
                {"name": "collateralId", "type": "uint256"},
                {"name": "collateralAmount", "type": "uint256"},
                {"name": "loanAssetAddress", "type": "address"},
                {"name": "loanAmount", "type": "uint256"},
                {"name": "loanYield", "type": "uint256"},
                {"name": "duration", "type": "uint32"},
                {"name": "expiration", "type": "uint40"},
                {"name": "borrower", "type": "address"},
                {"name": "lender", "type": "address"},
                {"name": "isPersistent", "type": "bool"},
                {"name": "nonce", "type": "uint256"},
            ],
        },
    }
    signable_message = encode_structured_data(offer_signable_message)

    contract = get_contract_class(offer_contract_address)

    offer_hash = Web3.to_hex(
        primitive=contract.getOfferHash(
            (
                offer_struct["collateralCategory"],
                offer_struct["collateralAddress"],
                offer_struct["collateralId"],
                offer_struct["collateralAmount"],
                offer_struct["loanAssetAddress"],
                offer_struct["loanAmount"],
                offer_struct["loanYield"],
                offer_struct["duration"],
                offer_struct["expiration"],
                offer_struct["borrower"],
                offer_struct["lender"],
                offer_struct["isPersistent"],
                offer_struct["nonce"],
            )
        )
    )

    signature = Web3().eth.account.sign_message(
        signable_message,
        private_key=TEST_AUTH_WALLET_PRIVATE_KEY,
    ).signature.hex()

    return offer_hash, requests.post(
        url=f"{API_BASE_URL}loan/offer/network/{chain_id}/{offer_contract_address}/",
        data={
            "loan_id": pwn_loan_id,
            "borrower_address": borrower_wallet_address,
            "lender_address": lender_wallet_address,
            "asset_address": loan_asset_contract_address,
            "asset_amount": loan_asset_amount,
            "loan_yield": loan_yield_amount,
            "duration": loan_duration_seconds,
            "expiration": offer_expiration_timestamp,
            "chain_id": chain_id,
            "contract_address": offer_contract_address,
            "nonce": offer_nonce,
            "hash": offer_hash,
            "signature": signature,
        },
        headers=dict(
            content_type="application/json",
            Authorization=f"Bearer {api_auth_token}",
        )
    )


def login(chain_id, private_key: bytes):
    pk = keys.PrivateKey(private_key)
    wallet_address = pk.public_key.to_checksum_address()

    nonce_message = get_auth_nonce(wallet_address)

    message = encode_defunct(primitive=nonce_message)
    signed_message = Web3().eth.account.sign_message(message, private_key=private_key)

    data = {
        "chain_id": chain_id,
        "wallet_address": wallet_address,
        "signature": signed_message.signature.hex(),
    }
    response = requests.post(
        f"{API_BASE_URL}web3auth/token/{wallet_address}/",
        data
    )
    return wallet_address, response.json()["access"]


if __name__ == "__main__":
    loan_requests = get_loan_requests(1, LOAN_CONTRACT_ADDRESS, "0xc3f733ca98E0daD0386979Eb96fb1722A1A05E69")
    wallet_address, access_token = login(CHAIN_ID, TEST_AUTH_WALLET_PRIVATE_KEY)

    for lr in loan_requests:
        offer_hash, response = post_loan(
            private_key=TEST_AUTH_WALLET_PRIVATE_KEY,
            chain_id=CHAIN_ID,
            offer_contract_address=OFFER_CONTRACT_ADDRESS,
            pwn_loan_id=lr["id"],
            api_auth_token=access_token,
            loan_asset_contract_address=DAI_CONTRACT_ADDRESS,
            borrower_wallet_address=lr["borrower_address"],
            lender_wallet_address=wallet_address,
            loan_asset_amount=LOAN_AMOUNT_WEI,
            loan_yield_amount=LOAN_YIELD_WEI,
            loan_duration_seconds=LOAN_DURATION_SECONDS,
            collateral_address=lr["collateral"]["contract"]["address"],
            collateral_token_id=lr["collateral"]["token_id"],
            collateral_amount=1,
            offer_expiration_timestamp=int((datetime.now(tz=timezone.utc) + timedelta(days=LOAN_VALIDITY_DAYS)).timestamp()),
        )
        print(f"{offer_hash}: {response.status}, {response.text}")
