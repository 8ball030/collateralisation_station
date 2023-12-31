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

"""This package contains the tests for rounds of CollateralisationStation."""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Hashable, List, Mapping, Type

import pytest

from packages.eightballer.skills.collateralisation_station_abci.rounds import (
    AbstractRound,
    CheckAvailableFundsRound,
    CheckForLoanRequestsRound,
    CheckOutstandingLoansRound,
    CheckValueOfCollateralRound,
    Event,
    InitialiseRound,
    PostTransactionRound,
    PrepareLiquidationRound,
    PrepareLoanOfferRound,
    PrepareUpdateRound,
    SynchronizedData,
)
from packages.valory.skills.abstract_round_abci.base import BaseTxPayload
from packages.valory.skills.abstract_round_abci.test_tools.rounds import BaseRoundTestClass


@dataclass
class RoundTestCase:
    """RoundTestCase"""

    name: str
    initial_data: Dict[str, Hashable]
    payloads: Mapping[str, BaseTxPayload]
    final_data: Dict[str, Hashable]
    event: Event
    synchronized_data_attr_checks: List[Callable] = field(default_factory=list)
    kwargs: Dict[str, Any] = field(default_factory=dict)


MAX_PARTICIPANTS: int = 4


class BaseCollateralisationStationRoundTest(BaseRoundTestClass):
    """Base test class for CollateralisationStation rounds."""

    round_cls: Type[AbstractRound]
    synchronized_data: SynchronizedData
    _synchronized_data_class = SynchronizedData
    _event_class = Event

    def run_test(self, test_case: RoundTestCase) -> None:
        """Run the test"""

        self.synchronized_data.update(**test_case.initial_data)

        test_round = self.round_cls(
            synchronized_data=self.synchronized_data,
        )

        self._complete_run(
            self._test_round(  # pylint: disable=no-member
                test_round=test_round,
                round_payloads=test_case.payloads,
                synchronized_data_update_fn=lambda sync_data, _: sync_data.update(**test_case.final_data),
                synchronized_data_attr_checks=test_case.synchronized_data_attr_checks,
                exit_event=test_case.event,
                **test_case.kwargs,  # varies per BaseRoundTestClass child
            )
        )


class TestCheckAvailableFundsRound(BaseCollateralisationStationRoundTest):
    """Tests for CheckAvailableFundsRound."""

    round_class = CheckAvailableFundsRound

    @pytest.mark.parametrize("test_case", [])
    def test_run(self, test_case: RoundTestCase) -> None:
        """Run tests."""

        self.run_test(test_case)


class TestCheckForLoanRequestsRound(BaseCollateralisationStationRoundTest):
    """Tests for CheckForLoanRequestsRound."""

    round_class = CheckForLoanRequestsRound

    @pytest.mark.parametrize("test_case", [])
    def test_run(self, test_case: RoundTestCase) -> None:
        """Run tests."""

        self.run_test(test_case)


class TestCheckOutstandingLoansRound(BaseCollateralisationStationRoundTest):
    """Tests for CheckOutstandingLoansRound."""

    round_class = CheckOutstandingLoansRound

    @pytest.mark.parametrize("test_case", [])
    def test_run(self, test_case: RoundTestCase) -> None:
        """Run tests."""

        self.run_test(test_case)


class TestCheckValueOfCollateralRound(BaseCollateralisationStationRoundTest):
    """Tests for CheckValueOfCollateralRound."""

    round_class = CheckValueOfCollateralRound

    @pytest.mark.parametrize("test_case", [])
    def test_run(self, test_case: RoundTestCase) -> None:
        """Run tests."""

        self.run_test(test_case)


class TestInitialiseRound(BaseCollateralisationStationRoundTest):
    """Tests for InitialiseRound."""

    round_class = InitialiseRound

    @pytest.mark.parametrize("test_case", [])
    def test_run(self, test_case: RoundTestCase) -> None:
        """Run tests."""

        self.run_test(test_case)


class TestPostTransactionRound(BaseCollateralisationStationRoundTest):
    """Tests for PostTransactionRound."""

    round_class = PostTransactionRound

    @pytest.mark.parametrize("test_case", [])
    def test_run(self, test_case: RoundTestCase) -> None:
        """Run tests."""

        self.run_test(test_case)


class TestPrepareLiquidationRound(BaseCollateralisationStationRoundTest):
    """Tests for PrepareLiquidationRound."""

    round_class = PrepareLiquidationRound

    @pytest.mark.parametrize("test_case", [])
    def test_run(self, test_case: RoundTestCase) -> None:
        """Run tests."""

        self.run_test(test_case)


class TestPrepareLoanOfferRound(BaseCollateralisationStationRoundTest):
    """Tests for PrepareLoanOfferRound."""

    round_class = PrepareLoanOfferRound

    @pytest.mark.parametrize("test_case", [])
    def test_run(self, test_case: RoundTestCase) -> None:
        """Run tests."""

        self.run_test(test_case)


class TestPrepareUpdateRound(BaseCollateralisationStationRoundTest):
    """Tests for PrepareUpdateRound."""

    round_class = PrepareUpdateRound

    @pytest.mark.parametrize("test_case", [])
    def test_run(self, test_case: RoundTestCase) -> None:
        """Run tests."""

        self.run_test(test_case)
