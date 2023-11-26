# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2023 eightballer
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""This package contains a scaffold of a model."""

from dataclasses import dataclass
from decimal import Decimal
from typing import Dict

from aea.skills.base import Model


@dataclass
class Ledger:
    """This class represents a ledger."""

    ledger_id: str
    chain_id: int
    chain_name: str
    explorer_url: str
    native_currency: str

    def __hash__(self) -> int:
        """
        hash the ledger id
        """
        return hash(self.ledger_id)


LEDGERS = [
    Ledger(
        ledger_id="ethereum",
        chain_id=1,
        chain_name="Ethereum",
        explorer_url="https://etherscan.io/",
        native_currency="ETH",
    ),
    Ledger(
        ledger_id="binance",
        chain_id=56,
        chain_name="Binance",
        explorer_url="https://bscscan.com/",
        native_currency="BNB",
    ),
    Ledger(
        ledger_id="gnosis",
        chain_id=100,
        chain_name="Gnosis",
        explorer_url="https://gnosisscan.io/",
        native_currency="XDAI",
    ),
    Ledger(
        ledger_id="matic",
        chain_id=137,
        chain_name="Matic",
        explorer_url="https://polygonscan.com/",
        native_currency="MATIC",
    ),
    Ledger(
        ledger_id="fantom",
        chain_id=250,
        chain_name="Fantom",
        explorer_url="https://ftmscan.com/",
        native_currency="FTM",
    ),
    Ledger(
        ledger_id="arbitrum",
        chain_id=42161,
        chain_name="Arbitrum",
        explorer_url="https://arbiscan.io/",
        native_currency="ETH",
    ),
    Ledger(
        ledger_id="avalanche",
        chain_id=43114,
        chain_name="Avalanche",
        explorer_url="https://cchain.explorer.avax.network/",
        native_currency="AVAX",
    ),
    Ledger(
        ledger_id="filecoin",
        chain_id=314,
        chain_name="Filecoin",
        explorer_url="https://filscan.io/",
        native_currency="FIL",
    ),
    Ledger(
        ledger_id="mantle",
        chain_id=5000,
        chain_name="Mantle",
        explorer_url="https://mantle.finance/",
        native_currency="MANTLE",
    ),
    Ledger(
        ledger_id="scroll",
        chain_id=534352,
        chain_name="Scroll",
        explorer_url="https://scrollscan.io/",
        native_currency="SCRL",
    ),
    Ledger(
        ledger_id="spark",
        chain_id=123,
        chain_name="Spark",
        explorer_url="https://sparkscan.io/",
        native_currency="SPARK",
    ),
]


LEDGERS = {ledger.ledger_id: ledger for ledger in LEDGERS}


@dataclass
class Balance:
    """This class represents a balance."""

    amount: int = -1
    decimals: int = 1e18


@dataclass
class Erc20Token:
    """This class represents an ERC20 token."""

    address: str
    name: str = None
    symbol: str = None
    decimals: int = None
    _balance: Balance = None

    @property
    def is_complete(self) -> bool:
        """Check if the token is complete."""
        return all(
            [
                self.address is not None,
                self.name is not None,
                self.symbol is not None,
                self.decimals is not None,
            ]
        )

    @property
    def balance_in_decimals(self) -> float:
        """Get the amount in decimals."""
        return Decimal(self.balance.amount / (10**self.decimals))

    @property
    def balance(self) -> Balance:
        """Get the balance."""
        if self._balance is None:
            return None
        return self._balance.amount

    @balance.setter
    def balance(self, value: int) -> None:
        """Set the balance."""
        self._balance = Balance(
            amount=value,
            decimals=self.decimals,
        )

    def __hash__(self) -> int:
        """
        hash the token address
        """
        return hash(self.address + self.name + self.symbol + str(self.decimals))


class BalanceMetricsStrategy(Model):
    """This class implements the balance metrics strategy."""

    ledgers: Dict[str, Ledger] = {}
    tokens: Dict[Ledger, Dict[str, Erc20Token]] = {}
    native_balances: Dict[Ledger, Balance] = {}
    prometheus_enabled: bool = False

    def __init__(self, **kwargs):
        """Initialize the balance metrics strategy."""
        ledgers = kwargs.pop("ledger_ids", {})
        for ledger_id in ledgers:
            if ledger_id not in LEDGERS:
                raise ValueError(f"Ledger id {ledger_id} not supported.")
            ledger = LEDGERS[ledger_id]
            self.ledgers[ledger_id] = ledger
            self.tokens[ledger] = {}
            self.native_balances[ledger] = Balance()
        self.ledgers = {ledger_id: LEDGERS[ledger_id] for ledger_id in ledgers}
        token_addresses = kwargs.pop("token_addresses", {})
        self.prometheus_enabled = kwargs.pop("prometheus_enabled", False)
        super().__init__(**kwargs)
        for ledger_id, addresses in token_addresses.items():
            ledger = self.ledgers.get(ledger_id)
            if ledger is None:
                self.context.logger.error(
                    f"Ledger id {ledger_id} not supported. Please add it to the `ledger_ids` parameter to monitor."
                )
                continue
            for address in addresses:
                token = Erc20Token(address)
                self.tokens[ledger][token.address] = token

        self.context.logger.info("Balance metrics strategy initialized.")
        self.context.logger.info(f"Ledgers: {self.ledgers}")
        self.context.logger.info(f"Tokens: {self.tokens}")
        self.context.shared_state["ledgers"] = self.ledgers
        self.context.shared_state["native_balances"] = self.native_balances