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

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Hashable, Optional, Type

import pytest

from packages.eightballer.skills.collateralisation_station_abci.behaviours import (
    CheckAvailableFundsBehaviour,
    CheckForLoanRequestsBehaviour,
    CheckOutstandingLoansBehaviour,
    CheckValueOfCollateralBehaviour,
    CollateralisationStationBaseBehaviour,
    CollateralisationStationRoundBehaviour,
    InitialiseBehaviour,
    PostTransactionBehaviour,
    PrepareLiquidationBehaviour,
    PrepareLoanOfferBehaviour,
    PrepareUpdateBehaviour,
)
from packages.eightballer.skills.collateralisation_station_abci.rounds import Event, SynchronizedData
from packages.valory.skills.abstract_round_abci.base import AbciAppDB
from packages.valory.skills.abstract_round_abci.behaviours import BaseBehaviour
from packages.valory.skills.abstract_round_abci.test_tools.base import FSMBehaviourBaseCase


@dataclass
class BehaviourTestCase:
    """BehaviourTestCase"""

    name: str
    initial_data: Dict[str, Hashable]
    event: Event
    kwargs: Dict[str, Any] = field(default_factory=dict)


class BaseCollateralisationStationTest(FSMBehaviourBaseCase):
    """Base test case."""

    path_to_skill = Path(__file__).parent.parent

    behaviour: CollateralisationStationRoundBehaviour
    behaviour_class: Type[CollateralisationStationBaseBehaviour]
    next_behaviour_class: Type[CollateralisationStationBaseBehaviour]
    synchronized_data: SynchronizedData
    done_event = Event.DONE

    @property
    def current_behaviour_id(self) -> str:
        """Current RoundBehaviour's behaviour id"""

        return self.behaviour.current_behaviour.behaviour_id

    def fast_forward(self, data: Optional[Dict[str, Any]] = None) -> None:
        """Fast-forward on initialization"""

        data = data if data is not None else {}
        self.fast_forward_to_behaviour(
            self.behaviour,
            self.behaviour_class.behaviour_id,
            SynchronizedData(AbciAppDB(setup_data=AbciAppDB.data_to_lists(data))),
        )
        assert self.current_behaviour_id == self.behaviour_class.behaviour_id

    def complete(self, event: Event) -> None:
        """Complete test"""

        self.behaviour.act_wrapper()
        self.mock_a2a_transaction()
        self._test_done_flag_set()
        self.end_round(done_event=event)
        assert self.current_behaviour_id == self.next_behaviour_class.behaviour_id


class TestCheckAvailableFundsBehaviour(BaseCollateralisationStationTest):
    """Tests CheckAvailableFundsBehaviour"""

    behaviour_class: Type[BaseBehaviour] = CheckAvailableFundsBehaviour
    next_behaviour_class: Type[BaseBehaviour] = ...

    @pytest.mark.parametrize("test_case", [])
    def test_run(self, test_case: BehaviourTestCase) -> None:
        """Run tests."""

        self.fast_forward(test_case.initial_data)
        # self.mock_ ...
        self.complete(test_case.event)


class TestCheckForLoanRequestsBehaviour(BaseCollateralisationStationTest):
    """Tests CheckForLoanRequestsBehaviour"""

    behaviour_class: Type[BaseBehaviour] = CheckForLoanRequestsBehaviour
    next_behaviour_class: Type[BaseBehaviour] = ...

    @pytest.mark.parametrize("test_case", [])
    def test_run(self, test_case: BehaviourTestCase) -> None:
        """Run tests."""

        self.fast_forward(test_case.initial_data)
        # self.mock_ ...
        self.complete(test_case.event)


class TestCheckOutstandingLoansBehaviour(BaseCollateralisationStationTest):
    """Tests CheckOutstandingLoansBehaviour"""

    behaviour_class: Type[BaseBehaviour] = CheckOutstandingLoansBehaviour
    next_behaviour_class: Type[BaseBehaviour] = ...

    @pytest.mark.parametrize("test_case", [])
    def test_run(self, test_case: BehaviourTestCase) -> None:
        """Run tests."""

        self.fast_forward(test_case.initial_data)
        # self.mock_ ...
        self.complete(test_case.event)


class TestCheckValueOfCollateralBehaviour(BaseCollateralisationStationTest):
    """Tests CheckValueOfCollateralBehaviour"""

    behaviour_class: Type[BaseBehaviour] = CheckValueOfCollateralBehaviour
    next_behaviour_class: Type[BaseBehaviour] = ...

    @pytest.mark.parametrize("test_case", [])
    def test_run(self, test_case: BehaviourTestCase) -> None:
        """Run tests."""

        self.fast_forward(test_case.initial_data)
        # self.mock_ ...
        self.complete(test_case.event)


class TestInitialiseBehaviour(BaseCollateralisationStationTest):
    """Tests InitialiseBehaviour"""

    behaviour_class: Type[BaseBehaviour] = InitialiseBehaviour
    next_behaviour_class: Type[BaseBehaviour] = ...

    @pytest.mark.parametrize("test_case", [])
    def test_run(self, test_case: BehaviourTestCase) -> None:
        """Run tests."""

        self.fast_forward(test_case.initial_data)
        # self.mock_ ...
        self.complete(test_case.event)


class TestPostTransactionBehaviour(BaseCollateralisationStationTest):
    """Tests PostTransactionBehaviour"""

    behaviour_class: Type[BaseBehaviour] = PostTransactionBehaviour
    next_behaviour_class: Type[BaseBehaviour] = ...

    @pytest.mark.parametrize("test_case", [])
    def test_run(self, test_case: BehaviourTestCase) -> None:
        """Run tests."""

        self.fast_forward(test_case.initial_data)
        # self.mock_ ...
        self.complete(test_case.event)


class TestPrepareLiquidationBehaviour(BaseCollateralisationStationTest):
    """Tests PrepareLiquidationBehaviour"""

    behaviour_class: Type[BaseBehaviour] = PrepareLiquidationBehaviour
    next_behaviour_class: Type[BaseBehaviour] = ...

    @pytest.mark.parametrize("test_case", [])
    def test_run(self, test_case: BehaviourTestCase) -> None:
        """Run tests."""

        self.fast_forward(test_case.initial_data)
        # self.mock_ ...
        self.complete(test_case.event)


class TestPrepareLoanOfferBehaviour(BaseCollateralisationStationTest):
    """Tests PrepareLoanOfferBehaviour"""

    behaviour_class: Type[BaseBehaviour] = PrepareLoanOfferBehaviour
    next_behaviour_class: Type[BaseBehaviour] = ...

    @pytest.mark.parametrize("test_case", [])
    def test_run(self, test_case: BehaviourTestCase) -> None:
        """Run tests."""

        self.fast_forward(test_case.initial_data)
        # self.mock_ ...
        self.complete(test_case.event)


class TestPrepareUpdateBehaviour(BaseCollateralisationStationTest):
    """Tests PrepareUpdateBehaviour"""

    behaviour_class: Type[BaseBehaviour] = PrepareUpdateBehaviour
    next_behaviour_class: Type[BaseBehaviour] = ...

    @pytest.mark.parametrize("test_case", [])
    def test_run(self, test_case: BehaviourTestCase) -> None:
        """Run tests."""

        self.fast_forward(test_case.initial_data)
        # self.mock_ ...
        self.complete(test_case.event)
