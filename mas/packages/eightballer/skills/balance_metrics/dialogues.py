from typing import Any, Type

from aea.common import Address
from aea.protocols.base import Message
from aea.protocols.dialogue.base import Dialogue as BaseDialogue
from aea.protocols.dialogue.base import DialogueLabel as BaseDialogueLabel
from aea.skills.base import Model

from packages.valory.protocols.contract_api.dialogues import (
    ContractApiDialogue as BaseContractApiDialogue,
)
from packages.valory.protocols.contract_api.dialogues import (
    ContractApiDialogues as BaseContractApiDialogues,
)
from packages.valory.protocols.contract_api.message import ContractApiMessage
from packages.valory.protocols.ledger_api.dialogues import (
    LedgerApiDialogue as BaseLedgerApiDialogue,
)
from packages.valory.protocols.ledger_api.dialogues import (
    LedgerApiDialogues as BaseLedgerApiDialogues,
)

from packages.eightballer.skills.prometheus.dialogues import (
    PrometheusDialogues as BasePrometheusDialogues,
)

PrometheusDialogues = BasePrometheusDialogues

class ContractApiDialogue(BaseContractApiDialogue):
    """The dialogue class maintains state of a dialogue and manages it."""

    __slots__ = ("_terms", "_associated_fipa_dialogue")

    def __init__(
        self,
        dialogue_label: BaseDialogueLabel,
        self_address: Address,
        role: BaseDialogue.Role,
        message_class: Type[ContractApiMessage] = ContractApiMessage,
    ) -> None:
        """
        Initialize a dialogue.

        :param dialogue_label: the identifier of the dialogue
        :param self_address: the address of the entity for whom this dialogue is maintained
        :param role: the role of the agent this dialogue is maintained for

        :return: None
        """
        BaseContractApiDialogue.__init__(
            self,
            dialogue_label=dialogue_label,
            self_address=self_address,
            role=role,
            message_class=message_class,
        )


LedgerApiDialogue = BaseLedgerApiDialogue


class LedgerApiDialogues(Model, BaseLedgerApiDialogues):
    """The dialogues class keeps track of all dialogues."""

    def __init__(self, **kwargs: Any) -> None:
        """
        Initialize dialogues.

        :return: None
        """
        Model.__init__(self, **kwargs)

        def role_from_first_message(  # pylint: disable=unused-argument
            message: Message, receiver_address: Address
        ) -> BaseDialogue.Role:
            """Infer the role of the agent from an incoming/outgoing first message

            :param message: an incoming/outgoing first message
            :param receiver_address: the address of the receiving agent
            :return: The role of the agent
            """
            del receiver_address, message
            return BaseLedgerApiDialogue.Role.AGENT

        BaseLedgerApiDialogues.__init__(
            self,
            self_address=str(self.skill_id),
            role_from_first_message=role_from_first_message,
        )


class ContractApiDialogues(Model, BaseContractApiDialogues):
    """The dialogues class keeps track of all dialogues."""

    def __init__(self, **kwargs: Any) -> None:
        """
        Initialize dialogues.

        :return: None
        """
        Model.__init__(self, **kwargs)

        def role_from_first_message(  # pylint: disable=unused-argument
            message: Message, receiver_address: Address
        ) -> BaseDialogue.Role:
            """Infer the role of the agent from an incoming/outgoing first message

            :param message: an incoming/outgoing first message
            :param receiver_address: the address of the receiving agent
            :return: The role of the agent
            """
            del receiver_address, message  # pragma: nocover
            return ContractApiDialogue.Role.AGENT

        BaseContractApiDialogues.__init__(
            self,
            self_address=str(self.skill_id),
            role_from_first_message=role_from_first_message,
            dialogue_class=ContractApiDialogue,
        )
