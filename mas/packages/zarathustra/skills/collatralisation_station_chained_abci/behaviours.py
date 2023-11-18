# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2023 Valory AG
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

"""This package contains round behaviours of ComposedAbciApp."""

from abc import ABC
from typing import Generator, Set, Type, cast

from packages.valory.skills.abstract_round_abci.base import AbstractRound
from packages.valory.skills.abstract_round_abci.behaviours import (
    AbstractRoundBehaviour,
    BaseBehaviour,
)

from packages.zarathustra.skills.collatralisation_station_chained_abci.models import Params
from packages.zarathustra.skills.collatralisation_station_chained_abci.rounds import (
    SynchronizedData,
    ComposedAbciApp,
    CheckAvailableFundsRound,
    CheckForLoanRequestsRound,
    CheckLateTxHashesRound,
    CheckOutstandingLoansRound,
    CheckTransactionHistoryRound,
    CheckValueOfCollateralRound,
    CollectSignatureRound,
    FinalizationRound,
    InitialiseRound,
    PostTransactionRound,
    PrepareLiquidationRound,
    PrepareLoanOfferRound,
    PrepareUpdateRound,
    RandomnessTransactionSubmissionRound,
    RegistrationRound,
    RegistrationStartupRound,
    ResetAndPauseRound,
    ResetRound,
    SelectKeeperTransactionSubmissionARound,
    SelectKeeperTransactionSubmissionBAfterTimeoutRound,
    SelectKeeperTransactionSubmissionBRound,
    SynchronizeLateMessagesRound,
    ValidateTransactionRound,
)
from packages.zarathustra.skills.collatralisation_station_chained_abci.rounds import (
    CheckAvailableFundsPayload,
    CheckForLoanRequestsPayload,
    CheckLateTxHashesPayload,
    CheckOutstandingLoansPayload,
    CheckTransactionHistoryPayload,
    CheckValueOfCollateralPayload,
    CollectSignaturePayload,
    FinalizationPayload,
    InitialisePayload,
    PostTransactionPayload,
    PrepareLiquidationPayload,
    PrepareLoanOfferPayload,
    PrepareUpdatePayload,
    RandomnessTransactionSubmissionPayload,
    RegistrationPayload,
    RegistrationStartupPayload,
    ResetAndPausePayload,
    ResetPayload,
    SelectKeeperTransactionSubmissionAPayload,
    SelectKeeperTransactionSubmissionBAfterTimeoutPayload,
    SelectKeeperTransactionSubmissionBPayload,
    SynchronizeLateMessagesPayload,
    ValidateTransactionPayload,
)


class ComposedBaseBehaviour(BaseBehaviour, ABC):
    """Base behaviour for the collatralisation_station_chained_abci skill."""

    @property
    def synchronized_data(self) -> SynchronizedData:
        """Return the synchronized data."""
        return cast(SynchronizedData, super().synchronized_data)

    @property
    def params(self) -> Params:
        """Return the params."""
        return cast(Params, super().params)


class CheckAvailableFundsBehaviour(ComposedBaseBehaviour):
    """CheckAvailableFundsBehaviour"""

    matching_round: Type[AbstractRound] = CheckAvailableFundsRound

    # TODO: implement logic required to set payload content for synchronization
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = CheckAvailableFundsPayload(sender=sender, content=...)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class CheckForLoanRequestsBehaviour(ComposedBaseBehaviour):
    """CheckForLoanRequestsBehaviour"""

    matching_round: Type[AbstractRound] = CheckForLoanRequestsRound

    # TODO: implement logic required to set payload content for synchronization
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = CheckForLoanRequestsPayload(sender=sender, content=...)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class CheckLateTxHashesBehaviour(ComposedBaseBehaviour):
    """CheckLateTxHashesBehaviour"""

    matching_round: Type[AbstractRound] = CheckLateTxHashesRound

    # TODO: implement logic required to set payload content for synchronization
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = CheckLateTxHashesPayload(sender=sender, content=...)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class CheckOutstandingLoansBehaviour(ComposedBaseBehaviour):
    """CheckOutstandingLoansBehaviour"""

    matching_round: Type[AbstractRound] = CheckOutstandingLoansRound

    # TODO: implement logic required to set payload content for synchronization
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = CheckOutstandingLoansPayload(sender=sender, content=...)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class CheckTransactionHistoryBehaviour(ComposedBaseBehaviour):
    """CheckTransactionHistoryBehaviour"""

    matching_round: Type[AbstractRound] = CheckTransactionHistoryRound

    # TODO: implement logic required to set payload content for synchronization
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = CheckTransactionHistoryPayload(sender=sender, content=...)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class CheckValueOfCollateralBehaviour(ComposedBaseBehaviour):
    """CheckValueOfCollateralBehaviour"""

    matching_round: Type[AbstractRound] = CheckValueOfCollateralRound

    # TODO: implement logic required to set payload content for synchronization
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = CheckValueOfCollateralPayload(sender=sender, content=...)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class CollectSignatureBehaviour(ComposedBaseBehaviour):
    """CollectSignatureBehaviour"""

    matching_round: Type[AbstractRound] = CollectSignatureRound

    # TODO: implement logic required to set payload content for synchronization
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = CollectSignaturePayload(sender=sender, content=...)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class FinalizationBehaviour(ComposedBaseBehaviour):
    """FinalizationBehaviour"""

    matching_round: Type[AbstractRound] = FinalizationRound

    # TODO: implement logic required to set payload content for synchronization
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = FinalizationPayload(sender=sender, content=...)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class InitialiseBehaviour(ComposedBaseBehaviour):
    """InitialiseBehaviour"""

    matching_round: Type[AbstractRound] = InitialiseRound

    # TODO: implement logic required to set payload content for synchronization
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = InitialisePayload(sender=sender, content=...)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class PostTransactionBehaviour(ComposedBaseBehaviour):
    """PostTransactionBehaviour"""

    matching_round: Type[AbstractRound] = PostTransactionRound

    # TODO: implement logic required to set payload content for synchronization
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = PostTransactionPayload(sender=sender, content=...)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class PrepareLiquidationBehaviour(ComposedBaseBehaviour):
    """PrepareLiquidationBehaviour"""

    matching_round: Type[AbstractRound] = PrepareLiquidationRound

    # TODO: implement logic required to set payload content for synchronization
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = PrepareLiquidationPayload(sender=sender, content=...)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class PrepareLoanOfferBehaviour(ComposedBaseBehaviour):
    """PrepareLoanOfferBehaviour"""

    matching_round: Type[AbstractRound] = PrepareLoanOfferRound

    # TODO: implement logic required to set payload content for synchronization
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = PrepareLoanOfferPayload(sender=sender, content=...)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class PrepareUpdateBehaviour(ComposedBaseBehaviour):
    """PrepareUpdateBehaviour"""

    matching_round: Type[AbstractRound] = PrepareUpdateRound

    # TODO: implement logic required to set payload content for synchronization
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = PrepareUpdatePayload(sender=sender, content=...)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class RandomnessTransactionSubmissionBehaviour(ComposedBaseBehaviour):
    """RandomnessTransactionSubmissionBehaviour"""

    matching_round: Type[AbstractRound] = RandomnessTransactionSubmissionRound

    # TODO: implement logic required to set payload content for synchronization
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = RandomnessTransactionSubmissionPayload(sender=sender, content=...)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class RegistrationBehaviour(ComposedBaseBehaviour):
    """RegistrationBehaviour"""

    matching_round: Type[AbstractRound] = RegistrationRound

    # TODO: implement logic required to set payload content for synchronization
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = RegistrationPayload(sender=sender, content=...)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class RegistrationStartupBehaviour(ComposedBaseBehaviour):
    """RegistrationStartupBehaviour"""

    matching_round: Type[AbstractRound] = RegistrationStartupRound

    # TODO: implement logic required to set payload content for synchronization
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = RegistrationStartupPayload(sender=sender, content=...)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class ResetAndPauseBehaviour(ComposedBaseBehaviour):
    """ResetAndPauseBehaviour"""

    matching_round: Type[AbstractRound] = ResetAndPauseRound

    # TODO: implement logic required to set payload content for synchronization
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = ResetAndPausePayload(sender=sender, content=...)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class ResetBehaviour(ComposedBaseBehaviour):
    """ResetBehaviour"""

    matching_round: Type[AbstractRound] = ResetRound

    # TODO: implement logic required to set payload content for synchronization
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = ResetPayload(sender=sender, content=...)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class SelectKeeperTransactionSubmissionABehaviour(ComposedBaseBehaviour):
    """SelectKeeperTransactionSubmissionABehaviour"""

    matching_round: Type[AbstractRound] = SelectKeeperTransactionSubmissionARound

    # TODO: implement logic required to set payload content for synchronization
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = SelectKeeperTransactionSubmissionAPayload(sender=sender, content=...)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class SelectKeeperTransactionSubmissionBAfterTimeoutBehaviour(ComposedBaseBehaviour):
    """SelectKeeperTransactionSubmissionBAfterTimeoutBehaviour"""

    matching_round: Type[AbstractRound] = SelectKeeperTransactionSubmissionBAfterTimeoutRound

    # TODO: implement logic required to set payload content for synchronization
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = SelectKeeperTransactionSubmissionBAfterTimeoutPayload(sender=sender, content=...)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class SelectKeeperTransactionSubmissionBBehaviour(ComposedBaseBehaviour):
    """SelectKeeperTransactionSubmissionBBehaviour"""

    matching_round: Type[AbstractRound] = SelectKeeperTransactionSubmissionBRound

    # TODO: implement logic required to set payload content for synchronization
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = SelectKeeperTransactionSubmissionBPayload(sender=sender, content=...)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class SynchronizeLateMessagesBehaviour(ComposedBaseBehaviour):
    """SynchronizeLateMessagesBehaviour"""

    matching_round: Type[AbstractRound] = SynchronizeLateMessagesRound

    # TODO: implement logic required to set payload content for synchronization
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = SynchronizeLateMessagesPayload(sender=sender, content=...)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class ValidateTransactionBehaviour(ComposedBaseBehaviour):
    """ValidateTransactionBehaviour"""

    matching_round: Type[AbstractRound] = ValidateTransactionRound

    # TODO: implement logic required to set payload content for synchronization
    def async_act(self) -> Generator:
        """Do the act, supporting asynchronous execution."""

        with self.context.benchmark_tool.measure(self.behaviour_id).local():
            sender = self.context.agent_address
            payload = ValidateTransactionPayload(sender=sender, content=...)

        with self.context.benchmark_tool.measure(self.behaviour_id).consensus():
            yield from self.send_a2a_transaction(payload)
            yield from self.wait_until_round_end()

        self.set_done()


class ComposedRoundBehaviour(AbstractRoundBehaviour):
    """ComposedRoundBehaviour"""

    initial_behaviour_cls = RegistrationStartupBehaviour
    abci_app_cls = ComposedAbciApp  # type: ignore
    behaviours: Set[Type[BaseBehaviour]] = [
        CheckAvailableFundsBehaviour,
        CheckForLoanRequestsBehaviour,
        CheckLateTxHashesBehaviour,
        CheckOutstandingLoansBehaviour,
        CheckTransactionHistoryBehaviour,
        CheckValueOfCollateralBehaviour,
        CollectSignatureBehaviour,
        FinalizationBehaviour,
        InitialiseBehaviour,
        PostTransactionBehaviour,
        PrepareLiquidationBehaviour,
        PrepareLoanOfferBehaviour,
        PrepareUpdateBehaviour,
        RandomnessTransactionSubmissionBehaviour,
        RegistrationBehaviour,
        RegistrationStartupBehaviour,
        ResetAndPauseBehaviour,
        ResetBehaviour,
        SelectKeeperTransactionSubmissionABehaviour,
        SelectKeeperTransactionSubmissionBAfterTimeoutBehaviour,
        SelectKeeperTransactionSubmissionBBehaviour,
        SynchronizeLateMessagesBehaviour,
        ValidateTransactionBehaviour
    ]
