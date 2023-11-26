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

"""This package contains a scaffold of a handler."""

from typing import Optional, cast

from aea.protocols.base import Message
from aea.skills.base import Handler

from packages.eightballer.skills.balance_metrics.dialogues import (
    ContractApiDialogue,
    ContractApiDialogues,
    LedgerApiDialogue,
    LedgerApiDialogues,
)
from packages.eightballer.skills.balance_metrics.strategy import BalanceMetricsStrategy
from packages.valory.protocols.contract_api.message import ContractApiMessage
from packages.valory.protocols.ledger_api.message import LedgerApiMessage

from packages.eightballer.skills.prometheus.handlers import PrometheusHandler as BasePrometheusHandler
from packages.eightballer.skills.prometheus.handlers import HttpHandler as BaseHttpHandler


PrometheusHandler = BasePrometheusHandler
HttpHandler = BaseHttpHandler


class ContractApiHandler(Handler):
    """Implement the contract api handler."""

    SUPPORTED_PROTOCOL = ContractApiMessage.protocol_id  # type: Optional[PublicId]

    def setup(self) -> None:
        """Implement the setup for the handler."""

    def handle(self, message: Message) -> None:
        """
        Implement the reaction to a message.
        :param message: the message
        :return: None
        """
        contract_api_msg = cast(ContractApiMessage, message)

        # recover dialogue
        contract_api_dialogues = cast(
            ContractApiDialogues, self.context.contract_api_dialogues
        )
        contract_api_dialogue = cast(
            Optional[ContractApiDialogue],
            contract_api_dialogues.update(contract_api_msg),
        )
        if contract_api_dialogue is None:
            self._handle_unidentified_dialogue(contract_api_msg)
            return

        # handle message
        if (
            contract_api_msg.performative
            is ContractApiMessage.Performative.RAW_TRANSACTION
        ):
            self._handle_raw_transaction(contract_api_msg, contract_api_dialogue)
        elif contract_api_msg.performative == ContractApiMessage.Performative.ERROR:
            self._handle_error(contract_api_msg, contract_api_dialogue)
        elif contract_api_msg.performative == ContractApiMessage.Performative.STATE:
            self._handle_state_update(contract_api_msg, contract_api_dialogue)
        else:
            self._handle_invalid(contract_api_msg, contract_api_dialogue)

    def teardown(self) -> None:
        """Tear down the handler."""

    def _handle_error(
        self,
        contract_api_msg: ContractApiMessage,
        contract_api_dialogue: ContractApiDialogue,
    ) -> None:
        """
        Handle an error message.

        :param contract_api_msg: the contract api message
        :param contract_api_dialogue: the dialogue
        """
        last_msg = contract_api_dialogue.last_outgoing_message

        self.context.logger.error(
            f"Error when trying to process contract call on ledger `{last_msg.ledger_id}` address=`{last_msg.contract_address}`, {last_msg.callable}, {last_msg.kwargs}"
        )
        self.context.logger.error(f"Error: {contract_api_msg}")

    def _handle_state_update(
        self,
        contract_api_msg: ContractApiMessage,
        contract_api_dialogue: ContractApiDialogue,
    ) -> None:
        """
        Handle a state update.

        :param contract_api_msg: the contract api message
        :param contract_api_dialogue: the dialogue
        """
        self.context.logger.info(f"State update: {contract_api_msg.state}")
        last_msg = contract_api_dialogue.last_outgoing_message
        ledger = self.strategy.ledgers.get(last_msg.ledger_id)
        token = self.strategy.tokens[ledger][last_msg.contract_address]
        if last_msg.callable in ["symbol", "decimals", "name"]:
            self.context.logger.debug(
                f"Updating token info for {last_msg.contract_address} callable: {last_msg.callable} data: {contract_api_msg.state}"
            )
            setattr(
                token,
                last_msg.callable,
                list(contract_api_msg.state.body.values()).pop(),
            )
        if last_msg.callable == "balance_of":
            self.context.logger.debug(
                f"Updating balance for {last_msg.contract_address} callable: {last_msg.callable} data: {contract_api_msg.state.body['int']}"
            )
            token.balance = contract_api_msg.state.body["int"]


    def setup(self) -> None:
        """Implement the setup for the handler."""
        self.strategy = cast(
            BalanceMetricsStrategy, self.context.balance_metrics_strategy
        )


class LedgerApiHandler(Handler):
    """This class scaffolds a handler."""

    SUPPORTED_PROTOCOL = LedgerApiMessage.protocol_id  # type: Optional[PublicId]

    def setup(self) -> None:
        """Implement the setup."""
        return

    def handle(self, message: Message) -> None:
        """
        Implement the reaction to an envelope.

        :param message: the message
        """
        ledger_api_msg = cast(LedgerApiMessage, message)
        strategy = cast(BalanceMetricsStrategy, self.context.balance_metrics_strategy)
        ledger_api_dialogues = cast(
            LedgerApiDialogues, self.context.ledger_api_dialogues
        )
        ledger_api_dialogue = cast(
            Optional[LedgerApiDialogue], ledger_api_dialogues.update(ledger_api_msg)
        )

        if ledger_api_msg.performative is LedgerApiMessage.Performative.BALANCE:
            ledger = strategy.ledgers.get(ledger_api_msg.ledger_id)
            current_balance = strategy.native_balances.get(ledger)
            current_balance.amount = ledger_api_msg.balance
            strategy.native_balances[ledger] = current_balance
            self.context.shared_state["native_balances"] = {i.ledger_id: i for i in strategy.native_balances}
            self.context.logger.debug(
                f"New Balance on {ledger.chain_name} is {current_balance}"
            )
        elif (
            ledger_api_msg.performative
            is LedgerApiMessage.Performative.TRANSACTION_DIGEST
        ):
            self._handle_transaction_digest(ledger_api_msg, ledger_api_dialogue)
        elif (
            ledger_api_msg.performative
            is LedgerApiMessage.Performative.TRANSACTION_RECEIPT
        ):
            self._handle_transaction_receipt(ledger_api_msg, ledger_api_dialogue)
        else:
            if ledger_api_msg.performative is LedgerApiMessage.Performative.ERROR:
                self.context.logger.error(
                    f"Error with the ledger message.\n{ledger_api_msg}"
                )
            else:
                if (
                    ledger_api_msg.performative
                    == LedgerApiMessage.Performative.RAW_TRANSACTION
                ):
                    # we need to sign the transaction
                    self._handle_raw_transaction(ledger_api_msg, ledger_api_dialogue)
                else:
                    raise NotImplementedError

    def teardown(self) -> None:
        """Tear down the handler."""
