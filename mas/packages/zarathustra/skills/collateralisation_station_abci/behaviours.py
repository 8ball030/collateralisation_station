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

"""This package contains round behaviours of CollateralisationStationAbciApp."""

from abc import ABC
from typing import Generator, Set, Type, cast

from packages.valory.skills.abstract_round_abci.base import AbstractRound
from packages.valory.skills.abstract_round_abci.behaviours import (
    AbstractRoundBehaviour,
    BaseBehaviour,
)

from packages.zarathustra.skills.collateralisation_station_abci.models import Params
from packages.zarathustra.skills.collateralisation_station_abci.rounds import (
    SynchronizedData,
    CollateralisationStationAbciApp,
    CheckAvailableFundsRound,
    CheckForLoanRequestsRound,
    CheckOutstandingLoansRound,
    CheckValueOfCollateralRound,
    InitialiseRound,
    PostTransactionRound,
    PrepareLiquidationRound,
    PrepareLoanOfferRound,
    PrepareUpdateRound,
)
from packages.zarathustra.skills.collateralisation_station_abci.rounds import (
    CheckAvailableFundsPayload,
    CheckForLoanRequestsPayload,
    CheckOutstandingLoansPayload,
    CheckValueOfCollateralPayload,
    InitialisePayload,
    PostTransactionPayload,
    PrepareLiquidationPayload,
    PrepareLoanOfferPayload,
    PrepareUpdatePayload,
)


class CollateralisationStationBaseBehaviour(BaseBehaviour, ABC):
    """Base behaviour for the collateralisation_station_abci skill."""

    @property
    def synchronized_data(self) -> SynchronizedData:
        """Return the synchronized data."""
        return cast(SynchronizedData, super().synchronized_data)

    @property
    def params(self) -> Params:
        """Return the params."""
        return cast(Params, super().params)


class CheckAvailableFundsBehaviour(CollateralisationStationBaseBehaviour):
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


class CheckForLoanRequestsBehaviour(CollateralisationStationBaseBehaviour):
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


class CheckOutstandingLoansBehaviour(CollateralisationStationBaseBehaviour):
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


class CheckValueOfCollateralBehaviour(CollateralisationStationBaseBehaviour):
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


class InitialiseBehaviour(CollateralisationStationBaseBehaviour):
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


class PostTransactionBehaviour(CollateralisationStationBaseBehaviour):
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


class PrepareLiquidationBehaviour(CollateralisationStationBaseBehaviour):
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


class PrepareLoanOfferBehaviour(CollateralisationStationBaseBehaviour):
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


class PrepareUpdateBehaviour(CollateralisationStationBaseBehaviour):
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


class CollateralisationStationRoundBehaviour(AbstractRoundBehaviour):
    """CollateralisationStationRoundBehaviour"""

    initial_behaviour_cls = InitialiseBehaviour
    abci_app_cls = CollateralisationStationAbciApp  # type: ignore
    behaviours: Set[Type[BaseBehaviour]] = [
        CheckAvailableFundsBehaviour,
        CheckForLoanRequestsBehaviour,
        CheckOutstandingLoansBehaviour,
        CheckValueOfCollateralBehaviour,
        InitialiseBehaviour,
        PostTransactionBehaviour,
        PrepareLiquidationBehaviour,
        PrepareLoanOfferBehaviour,
        PrepareUpdateBehaviour
    ]
