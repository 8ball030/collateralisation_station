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

"""package contains a scaffold of the handler for the Attestation Handler skill."""

from typing import cast

from aea.protocols.base import Message

from packages.eightballer.skills.attestation_client.dialogues import (
    TendermintDialogue,
    TendermintDialogues,
)
from packages.eightballer.skills.attestation_client.strategy import (
    AttestationClientModel,
)
from packages.valory.protocols.tendermint.message import TendermintMessage
from packages.valory.skills.abstract_round_abci.handlers import (
    TendermintHandler as BaseTendermintHandler,
)


class AttestationTendermintHandler(BaseTendermintHandler):
    """class enables paritcipant to reply to attestations from the attestation service."""

    def handle(self, message: Message) -> None:
        """
        Implement the reaction to an envelope.

        :param message: the message
        """

        strategy = cast(AttestationClientModel, self.context.attestation_strategy)
        if strategy.attestation_enabled:
            if not self._handle_attestation(message):
                super().handle(message)
        else:
            super().handle(message)

    def _handle_attestation(self, message: Message) -> bool:
        """
        We handle the tendermint message.
        If the message is in the list of attestor addresses, we reply with the recovery params.
        :param message: the message
        :return: whether the message is handled or not.
        """
        message = cast(TendermintMessage, message)

        if all(
            [
                message.performative
                == TendermintMessage.Performative.GET_RECOVERY_PARAMS,
                message.sender in self.context.strategy.attestor_addresses,
            ]
        ):
            dialogues = cast(TendermintDialogues, self.dialogues)
            dialogue = cast(TendermintDialogue, dialogues.update(message))
            self._get_recovery_params(message, dialogue)
            return True
        return False
