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

"""This module contains the transaction payloads of the CollateralisationStationAbciApp."""

from dataclasses import dataclass

from packages.valory.skills.abstract_round_abci.base import BaseTxPayload


@dataclass(frozen=True)
class CheckAvailableFundsPayload(BaseTxPayload):
    """Represent a transaction payload for the CheckAvailableFundsRound."""


@dataclass(frozen=True)
class CheckForLoanRequestsPayload(BaseTxPayload):
    """Represent a transaction payload for the CheckForLoanRequestsRound."""


@dataclass(frozen=True)
class CheckOutstandingLoansPayload(BaseTxPayload):
    """Represent a transaction payload for the CheckOutstandingLoansRound."""


@dataclass(frozen=True)
class CheckValueOfCollateralPayload(BaseTxPayload):
    """Represent a transaction payload for the CheckValueOfCollateralRound."""


@dataclass(frozen=True)
class InitialisePayload(BaseTxPayload):
    """Represent a transaction payload for the InitialiseRound."""


@dataclass(frozen=True)
class PostTransactionPayload(BaseTxPayload):
    """Represent a transaction payload for the PostTransactionRound."""


@dataclass(frozen=True)
class PrepareLiquidationPayload(BaseTxPayload):
    """Represent a transaction payload for the PrepareLiquidationRound."""


@dataclass(frozen=True)
class PrepareLoanOfferPayload(BaseTxPayload):
    """Represent a transaction payload for the PrepareLoanOfferRound."""


@dataclass(frozen=True)
class PrepareUpdatePayload(BaseTxPayload):
    """Represent a transaction payload for the PrepareUpdateRound."""
