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

"""This package contains a scaffold of a behaviour."""

from typing import Any, Dict, cast

from packages.eightballer.contracts.erc_20 import PUBLIC_ID as ERC_20_PUBLIC_ID
from packages.eightballer.skills.balance_metrics.dialogues import (
    ContractApiDialogues,
    LedgerApiDialogues,
)
from packages.eightballer.skills.balance_metrics.strategy import (
    BalanceMetricsStrategy,
    Ledger,
)
from packages.eightballer.skills.prometheus.behaviours import PrometheusBehaviour
from packages.valory.connections.ledger.connection import (
    PUBLIC_ID as LEDGER_CONNECTION_PUBLIC_ID,
)
from packages.valory.protocols.contract_api.custom_types import Kwargs
from packages.valory.protocols.contract_api.message import ContractApiMessage
from packages.valory.protocols.ledger_api.message import LedgerApiMessage

LEDGER_API_ADDRESS = str(LEDGER_CONNECTION_PUBLIC_ID)


class BalancePollingBehaviour(PrometheusBehaviour):
    """This class scaffolds a behaviour."""

    strategy: BalanceMetricsStrategy
    tokens_added_to_prometheus: set = {}

    def setup(self) -> None:
        """Implement the setup."""
        self.strategy = cast(
            BalanceMetricsStrategy, self.context.balance_metrics_strategy
        )
        # we need to send the initial message to the ledger API to get information about the token.
        self.request_all_token_info()
        super().setup()

    def act(self) -> None:
        """Implement the act."""

        for ledger in self.strategy.tokens.keys():
            for token in self.strategy.tokens[ledger].values():
                metric_name = to_metric_name(ledger, token)
                if not token.is_complete:
                    # we have not yet received the token info, so we do nothing.
                    continue
                else:
                    if (
                        token not in self.tokens_added_to_prometheus
                        and self.strategy.prometheus_enabled
                    ):
                        self.context.logger.info(
                            f"Adding token {token.address} to prometheus"
                        )
                        msg, dialogue = self.add_prometheus_metric(
                            metric_name,
                            "Gauge",
                            f"Balance of {token.symbol} on {ledger.chain_name}",
                            {
                                "agent_address": self.context.agent_address,
                            },
                        )
                        self.tokens_added_to_prometheus[token] = token
                    else:
                        self.request_erc20_balance(token.address)
                        if self.strategy.prometheus_enabled and token.balance is not None:
                            self.update_prometheus_metric(
                                metric_name=metric_name,
                                update_func="set",
                                value=token.balance / 10 ** token.decimals,
                                labels={"agent_address": self.context.agent_address, 
                                        "token_address": token.address,
                                        "token_name": token.name,
                                        "ledger": ledger.chain_name,
                                        },
                            )

        # we do the same for the native balance.
        for ledger in self.strategy.ledgers.values():
            metric_name = to_metric_name(ledger)
            if (
                ledger not in self.tokens_added_to_prometheus
                and self.strategy.prometheus_enabled
            ):
                self.context.logger.info(
                    f"Adding ledger {ledger.chain_name} to prometheus"
                )
                self.add_prometheus_metric(
                    metric_name,
                    "Gauge",
                    f"Balance of {ledger.native_currency} on {ledger.chain_name}",
                    {
                        "agent_address": self.context.agent_address,
                    },
                )
                self.tokens_added_to_prometheus[ledger] = ledger
            else:
                self.request_native_token_info(ledger)
                balance = self.strategy.native_balances.get(ledger)
                if balance is not None:
                    if balance.amount is not None:
                        self.update_prometheus_metric(
                            metric_name=metric_name,
                            update_func="set",
                            value=float(balance.amount * 10 ** 18),
                            labels={"agent_address": self.context.agent_address, 
                                    "ledger": ledger.chain_name,
                                    },
                        )
        super().act()
        self.context.shared_state["balances"] = {
            k.ledger_id: v for k, v in self.strategy.native_balances.items()
        }

    def teardown(self) -> None:
        """Implement the task teardown."""

    def request_all_token_info(self):
        """
        For each of the ledgers, request the token info.
        """
        for ledger, tokens in self.strategy.tokens.items():
            # we request the native token info
            self.context.logger.info(f"requesting info for {ledger} native token")
            self.request_native_token_info(ledger)
            for token in tokens.values():
                self.context.logger.info(f"Requesting info for {token.address}")
                self.request_token_info(ledger, token.address)

    def __init__(self, tick_interval: float = 5, **kwargs: Any) -> None:
        super().__init__(tick_interval=tick_interval, **kwargs)

    def request_native_token_info(self, ledger: Ledger) -> None:
        """
        We create a request message for the ledger API to get the native token info.
        """
        ledger_api_dialogues = cast(
            LedgerApiDialogues, self.context.ledger_api_dialogues
        )
        ledger_api_msg, _ = ledger_api_dialogues.create(
            counterparty=LEDGER_API_ADDRESS,
            performative=LedgerApiMessage.Performative.GET_BALANCE,
            ledger_id=ledger.ledger_id,
            address=self.context.agent_address,
        )
        self.context.logger.debug(
            f"Requesting token info for {ledger.chain_name} native token"
        )
        self.context.outbox.put_message(message=ledger_api_msg)

    def request_token_info(self, ledger: Ledger, token_address: str) -> None:
        """
        We create a request message for the Contract API to get the token info.
        """
        for func_name in ["symbol", "decimals", "name"]:
            contract_api_dialogues = cast(
                ContractApiDialogues, self.context.contract_api_dialogues
            )
            contract_api_msg, _ = contract_api_dialogues.create(
                counterparty=LEDGER_API_ADDRESS,
                performative=ContractApiMessage.Performative.GET_STATE,
                contract_id=str(ERC_20_PUBLIC_ID),
                ledger_id=ledger.ledger_id,
                contract_address=token_address,
                callable=func_name,
                kwargs=Kwargs({}),
            )
            self.context.outbox.put_message(message=contract_api_msg)
        self.context.logger.debug(f"Requesting token info for {token_address}")

    def request_erc20_balance(self, token_address: str) -> None:
        """
        We create a request message for the Contract API to get the balance of the token.
        """
        for ledger in self.strategy.tokens.keys():
            contract_api_dialogues = cast(
                ContractApiDialogues, self.context.contract_api_dialogues
            )
            contract_api_msg, _ = contract_api_dialogues.create(
                counterparty=LEDGER_API_ADDRESS,
                performative=ContractApiMessage.Performative.GET_STATE,
                contract_id=str(ERC_20_PUBLIC_ID),
                ledger_id=ledger.ledger_id,
                contract_address=token_address,
                callable="balance_of",
                kwargs=Kwargs({"account": self.context.agent_address}),
            )
            self.context.outbox.put_message(message=contract_api_msg)
            self.context.logger.debug(f"Requesting balance of {token_address}")


def to_metric_name(ledger,
                   token=None,
                   ):
    """
    Convert a ledger and token to a metric name.
    If the token is None, then the metric name is the ledger name.
    """
    base_token_name = f"{ledger.chain_name}"
    if token is None:
        name = f"{base_token_name}_native_balance".replace(" ", "_")
    else:
        name = f"{base_token_name}_{token.name}_{token.symbol}_balance"
    return name.lower().replace("(", "_").replace(")", "_").replace(" ", "_")
         
    

