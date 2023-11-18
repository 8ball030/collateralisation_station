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

from packages.valory.skills.abstract_round_abci.base import (
    AbciApp,
    AbciAppTransitionFunction,
    AbstractRound,
    AppState,
    BaseSynchronizedData,
    DegenerateRound,
    EventToTimeout,
    get_name,
)
from packages.zarathustra.skills.collateralisation_station_abci.payloads import (
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


class Event(Enum):
    """CollateralisationStationAbciApp Events"""

    LOAN_REQUESTS_EXIST = "loan_requests_exist"
    WORTHLESS_NFT = "worthless_nft"
    DONE = "done"
    OFFERABLE_NFT = "offerable_nft"
    POST_UPDATE = "post_update"
    SUFFICIENT_FUNDS = "sufficient_funds"
    ALREADY_OFFERED = "already_offered"
    NO_LOANS_REQUESTS = "no_loans_requests"
    LOAN_NOT_PAID = "loan_not_paid"
    INSUFFICIENT_FUNDS = "insufficient_funds"


class SynchronizedData(BaseSynchronizedData):
    """
    Class to represent the synchronized data.

    This data is replicated by the tendermint application.
    """

    @property
    def most_voted_tx_hash(self) -> float:
        """Get the most_voted_tx_hash."""
        return cast(float, self.db.get_strict("most_voted_tx_hash"))


class CheckAvailableFundsRound(AbstractRound):
    """CheckAvailableFundsRound"""

    payload_class = CheckAvailableFundsPayload
    payload_attribute = ""  # TODO: update
    synchronized_data_class = SynchronizedData

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""
        synchronized_data = self.synchronized_data
        return synchronized_data, Event.SUFFICIENT_FUNDS

    def check_payload(self, payload: CheckAvailableFundsPayload) -> None:
        """Check payload."""
        raise NotImplementedError

    def process_payload(self, payload: CheckAvailableFundsPayload) -> None:
        """Process payload."""
        raise NotImplementedError


class CheckForLoanRequestsRound(AbstractRound):
    """CheckForLoanRequestsRound"""

    payload_class = CheckForLoanRequestsPayload
    payload_attribute = ""  # TODO: update
    synchronized_data_class = SynchronizedData

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""
        synchronized_data = self.synchronized_data
        return synchronized_data, Event.LOAN_REQUESTS_EXIST

    def check_payload(self, payload: CheckForLoanRequestsPayload) -> None:
        """Check payload."""
        raise NotImplementedError

    def process_payload(self, payload: CheckForLoanRequestsPayload) -> None:
        """Process payload."""
        raise NotImplementedError


class CheckOutstandingLoansRound(AbstractRound):
    """CheckOutstandingLoansRound"""

    payload_class = CheckOutstandingLoansPayload
    payload_attribute = ""  # TODO: update
    synchronized_data_class = SynchronizedData

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""
        synchronized_data = self.synchronized_data
        return synchronized_data, Event.DONE

    def check_payload(self, payload: CheckOutstandingLoansPayload) -> None:
        """Check payload."""
        raise NotImplementedError

    def process_payload(self, payload: CheckOutstandingLoansPayload) -> None:
        """Process payload."""
        raise NotImplementedError


class CheckValueOfCollateralRound(AbstractRound):
    """CheckValueOfCollateralRound"""

    payload_class = CheckValueOfCollateralPayload
    payload_attribute = ""  # TODO: update
    synchronized_data_class = SynchronizedData

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""
        synchronized_data = self.synchronized_data
        return synchronized_data, Event.OFFERABLE_NFT

    def check_payload(self, payload: CheckValueOfCollateralPayload) -> None:
        """Check payload."""
        raise NotImplementedError

    def process_payload(self, payload: CheckValueOfCollateralPayload) -> None:
        """Process payload."""
        raise NotImplementedError


class InitialiseRound(AbstractRound):
    """InitialiseRound"""

    payload_class = InitialisePayload
    payload_attribute = ""  # TODO: update
    synchronized_data_class = SynchronizedData

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""
        synchronized_data = self.synchronized_data
        return synchronized_data, Event.DONE

    def check_payload(self, payload: InitialisePayload) -> None:
        """Check payload."""
        raise NotImplementedError

    def process_payload(self, payload: InitialisePayload) -> None:
        """Process payload."""
        raise NotImplementedError


class PostTransactionRound(AbstractRound):
    """PostTransactionRound"""

    payload_class = PostTransactionPayload
    payload_attribute = ""  # TODO: update
    synchronized_data_class = SynchronizedData

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""
        synchronized_data = self.synchronized_data
        return synchronized_data, Event.DONE

    def check_payload(self, payload: PostTransactionPayload) -> None:
        """Check payload."""
        raise NotImplementedError

    def process_payload(self, payload: PostTransactionPayload) -> None:
        """Process payload."""
        raise NotImplementedError


class PrepareLiquidationRound(AbstractRound):
    """PrepareLiquidationRound"""

    payload_class = PrepareLiquidationPayload
    payload_attribute = ""  # TODO: update
    synchronized_data_class = SynchronizedData

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""
        synchronized_data = self.synchronized_data
        return synchronized_data, Event.DONE

    def check_payload(self, payload: PrepareLiquidationPayload) -> None:
        """Check payload."""
        raise NotImplementedError

    def process_payload(self, payload: PrepareLiquidationPayload) -> None:
        """Process payload."""
        raise NotImplementedError


class PrepareLoanOfferRound(AbstractRound):
    """PrepareLoanOfferRound"""

    payload_class = PrepareLoanOfferPayload
    payload_attribute = ""  # TODO: update
    synchronized_data_class = SynchronizedData

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""
        synchronized_data = self.synchronized_data
        return synchronized_data, Event.DONE

    def check_payload(self, payload: PrepareLoanOfferPayload) -> None:
        """Check payload."""
        raise NotImplementedError

    def process_payload(self, payload: PrepareLoanOfferPayload) -> None:
        """Process payload."""
        raise NotImplementedError


class PrepareUpdateRound(AbstractRound):
    """PrepareUpdateRound"""

    payload_class = PrepareUpdatePayload
    payload_attribute = ""  # TODO: update
    synchronized_data_class = SynchronizedData

    def end_block(self) -> Optional[Tuple[BaseSynchronizedData, Enum]]:
        """Process the end of the block."""
        synchronized_data = self.synchronized_data
        return synchronized_data, Event.POST_UPDATE

    def check_payload(self, payload: PrepareUpdatePayload) -> None:
        """Check payload."""
        raise NotImplementedError

    def process_payload(self, payload: PrepareUpdatePayload) -> None:
        """Process payload."""
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
    initial_states: Set[AppState] = {InitialiseRound, PostTransactionRound}
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
        PrepareOfferTxSubmissionRound: {},
        PrepareUpdateTxSubmissionRound: {},
        PrepareLiquidationTxSubmissionRound: {},
        FinishedRound: {},
    }
    final_states: Set[AppState] = {
        PrepareUpdateTxSubmissionRound,
        PrepareLiquidationTxSubmissionRound,
        PrepareOfferTxSubmissionRound,
        FinishedRound,
    }
    event_to_timeout: EventToTimeout = {}
    cross_period_persisted_keys: Set[str] = set()
    db_pre_conditions: Dict[AppState, Set[str]] = {
        InitialiseRound: {get_name(SynchronizedData.participants)},
        PostTransactionRound: {get_name(SynchronizedData.participants)},
    }
    db_post_conditions: Dict[AppState, Set[str]] = {
        PrepareUpdateTxSubmissionRound: {get_name(SynchronizedData.most_voted_tx_hash)},
        PrepareLiquidationTxSubmissionRound: {get_name(SynchronizedData.most_voted_tx_hash)},
        PrepareOfferTxSubmissionRound: {get_name(SynchronizedData.most_voted_tx_hash)},
        FinishedRound: set(),
    }
