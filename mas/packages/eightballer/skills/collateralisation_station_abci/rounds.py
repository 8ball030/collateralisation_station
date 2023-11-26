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

"""This package contains the rounds of CollateralisationStationAbciApp."""

from enum import Enum
from typing import Dict, Optional, Set, Tuple

from packages.eightballer.skills.collateralisation_station_abci.payloads import (
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
from packages.valory.skills.abstract_round_abci.base import (
    AbciApp,
    AbciAppTransitionFunction,
    AbstractRound,
    AppState,
    BaseSynchronizedData,
    DegenerateRound,
    EventToTimeout,
)


class Event(Enum):
    """CollateralisationStationAbciApp Events"""

    POST_UPDATE = "post_update"
    DONE = "done"
    LOAN_NOT_PAID = "loan_not_paid"
    LOAN_REQUESTS_EXIST = "loan_requests_exist"
    ALREADY_OFFERED = "already_offered"
    SUFFICIENT_FUNDS = "sufficient_funds"
    INSUFFICIENT_FUNDS = "insufficient_funds"
    WORTHLESS_NFT = "worthless_nft"
    OFFERABLE_NFT = "offerable_nft"
    NO_LOANS_REQUESTS = "no_loans_requests"


class SynchronizedData(BaseSynchronizedData):
    """
    Class to represent the synchronized data.

    This data is replicated by the tendermint application.
    """


class CheckAvailableFundsRound(AbstractRound):
    """CheckAvailableFundsRound"""

    payload_class = CheckAvailableFundsPayload
    payload_attribute = ""
    synchronized_data_class = SynchronizedData

    # CollectSameUntilAllRound, CollectSameUntilThresholdRound,
    # CollectDifferentUntilThresholdRound, OnlyKeeperSendsRound, VotingRound,
    # from packages/valory/skills/abstract_round_abci/base.py
    # or implement the methods

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""
        raise NotImplementedError


class CheckForLoanRequestsRound(AbstractRound):
    """CheckForLoanRequestsRound"""

    payload_class = CheckForLoanRequestsPayload
    payload_attribute = ""
    synchronized_data_class = SynchronizedData

    # CollectSameUntilAllRound, CollectSameUntilThresholdRound,
    # CollectDifferentUntilThresholdRound, OnlyKeeperSendsRound, VotingRound,
    # from packages/valory/skills/abstract_round_abci/base.py
    # or implement the methods

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""
        raise NotImplementedError


class CheckOutstandingLoansRound(AbstractRound):
    """CheckOutstandingLoansRound"""

    payload_class = CheckOutstandingLoansPayload
    payload_attribute = ""
    synchronized_data_class = SynchronizedData

    # CollectSameUntilAllRound, CollectSameUntilThresholdRound,
    # CollectDifferentUntilThresholdRound, OnlyKeeperSendsRound, VotingRound,
    # from packages/valory/skills/abstract_round_abci/base.py
    # or implement the methods

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""
        raise NotImplementedError


class CheckValueOfCollateralRound(AbstractRound):
    """CheckValueOfCollateralRound"""

    payload_class = CheckValueOfCollateralPayload
    payload_attribute = ""
    synchronized_data_class = SynchronizedData

    # CollectSameUntilAllRound, CollectSameUntilThresholdRound,
    # CollectDifferentUntilThresholdRound, OnlyKeeperSendsRound, VotingRound,
    # from packages/valory/skills/abstract_round_abci/base.py
    # or implement the methods

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""
        raise NotImplementedError


class InitialiseRound(AbstractRound):
    """InitialiseRound"""

    payload_class = InitialisePayload
    payload_attribute = ""
    synchronized_data_class = SynchronizedData

    # CollectSameUntilAllRound, CollectSameUntilThresholdRound,
    # CollectDifferentUntilThresholdRound, OnlyKeeperSendsRound, VotingRound,
    # from packages/valory/skills/abstract_round_abci/base.py
    # or implement the methods

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""
        raise NotImplementedError


class PostTransactionRound(AbstractRound):
    """PostTransactionRound"""

    payload_class = PostTransactionPayload
    payload_attribute = ""
    synchronized_data_class = SynchronizedData

    # CollectSameUntilAllRound, CollectSameUntilThresholdRound,
    # CollectDifferentUntilThresholdRound, OnlyKeeperSendsRound, VotingRound,
    # from packages/valory/skills/abstract_round_abci/base.py
    # or implement the methods

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""
        raise NotImplementedError


class PrepareLiquidationRound(AbstractRound):
    """PrepareLiquidationRound"""

    payload_class = PrepareLiquidationPayload
    payload_attribute = ""
    synchronized_data_class = SynchronizedData

    # CollectSameUntilAllRound, CollectSameUntilThresholdRound,
    # CollectDifferentUntilThresholdRound, OnlyKeeperSendsRound, VotingRound,
    # from packages/valory/skills/abstract_round_abci/base.py
    # or implement the methods

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""
        raise NotImplementedError


class PrepareLoanOfferRound(AbstractRound):
    """PrepareLoanOfferRound"""

    payload_class = PrepareLoanOfferPayload
    payload_attribute = ""
    synchronized_data_class = SynchronizedData

    # CollectSameUntilAllRound, CollectSameUntilThresholdRound,
    # CollectDifferentUntilThresholdRound, OnlyKeeperSendsRound, VotingRound,
    # from packages/valory/skills/abstract_round_abci/base.py
    # or implement the methods

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""
        raise NotImplementedError


class PrepareUpdateRound(AbstractRound):
    """PrepareUpdateRound"""

    payload_class = PrepareUpdatePayload
    payload_attribute = ""
    synchronized_data_class = SynchronizedData

    # CollectSameUntilAllRound, CollectSameUntilThresholdRound,
    # CollectDifferentUntilThresholdRound, OnlyKeeperSendsRound, VotingRound,
    # from packages/valory/skills/abstract_round_abci/base.py
    # or implement the methods

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""
        raise NotImplementedError


class FinishedRound(DegenerateRound):
    """FinishedRound"""


class PrepareLiquidationTxSubmissionRound(DegenerateRound):
    """PrepareLiquidationTxSubmissionRound"""


class PrepareOfferTxSubmissionRound(DegenerateRound):
    """PrepareOfferTxSubmissionRound"""


class PrepareUpdateTxSubmissionRound(DegenerateRound):
    """PrepareUpdateTxSubmissionRound"""


class CollateralisationStationAbciApp(AbciApp[Event]):
    """CollateralisationStationAbciApp"""

    initial_round_cls: AppState = InitialiseRound
    initial_states: Set[AppState] = {PostTransactionRound, InitialiseRound}
    transition_function: AbciAppTransitionFunction = {
        InitialiseRound: {Event.DONE: CheckOutstandingLoansRound},
        PostTransactionRound: {Event.DONE: PrepareUpdateRound},
        PrepareUpdateRound: {Event.DONE: PrepareUpdateTxSubmissionRound, Event.POST_UPDATE: CheckOutstandingLoansRound},
        CheckOutstandingLoansRound: {
            Event.DONE: CheckForLoanRequestsRound,
            Event.LOAN_NOT_PAID: PrepareLiquidationRound,
        },
        PrepareLiquidationRound: {Event.DONE: PrepareLiquidationTxSubmissionRound},
        CheckForLoanRequestsRound: {
            Event.ALREADY_OFFERED: FinishedRound,
            Event.NO_LOANS_REQUESTS: FinishedRound,
            Event.LOAN_REQUESTS_EXIST: CheckAvailableFundsRound,
        },
        CheckAvailableFundsRound: {
            Event.SUFFICIENT_FUNDS: CheckValueOfCollateralRound,
            Event.INSUFFICIENT_FUNDS: FinishedRound,
        },
        CheckValueOfCollateralRound: {Event.OFFERABLE_NFT: PrepareLoanOfferRound, Event.WORTHLESS_NFT: FinishedRound},
        PrepareLoanOfferRound: {Event.DONE: PrepareOfferTxSubmissionRound},
        FinishedRound: {},
        PrepareOfferTxSubmissionRound: {},
        PrepareLiquidationTxSubmissionRound: {},
        PrepareUpdateTxSubmissionRound: {},
    }
    final_states: Set[AppState] = {
        FinishedRound,
        PrepareOfferTxSubmissionRound,
        PrepareUpdateTxSubmissionRound,
        PrepareLiquidationTxSubmissionRound,
    }
    event_to_timeout: EventToTimeout = {}
    cross_period_persisted_keys: Set[str] = []
    db_pre_conditions: Dict[AppState, Set[str]] = {
        PostTransactionRound: [],
        InitialiseRound: [],
    }
    db_post_conditions: Dict[AppState, Set[str]] = {
        FinishedRound: [],
        PrepareOfferTxSubmissionRound: [],
        PrepareUpdateTxSubmissionRound: [],
        PrepareLiquidationTxSubmissionRound: [],
    }
