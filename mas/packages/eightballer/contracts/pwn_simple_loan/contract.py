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

"""This module contains the scaffold contract definition."""

from typing import Any

from aea.common import JSONLike
from packages.eightballer.contracts.pwn_simple_loan import PUBLIC_ID
from aea.contracts.base import Contract
from aea.crypto.base import LedgerApi, Address


class PwnSimpleLoan(Contract):
    """The scaffold contract class for a smart contract."""

    contract_id = PUBLIC_ID


    @classmethod
    def min_loan_duration(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        
        ) -> JSONLike:
        """Handler method for the 'min_loan_duration' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.MIN_LOAN_DURATION().call()
        return {
            'int': result
        }



    @classmethod
    def encode_loan_terms_factory_data(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        offer: tuple
        ) -> JSONLike:
        """Handler method for the 'encode_loan_terms_factory_data' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.encodeLoanTermsFactoryData(offer=offer).call()
        return {
            'str': result
        }



    @classmethod
    def get_offer_hash(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        offer: tuple
        ) -> JSONLike:
        """Handler method for the 'get_offer_hash' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.getOfferHash(offer=offer).call()
        return {
            'str': result
        }



    @classmethod
    def offers_made(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        var_0: str
        ) -> JSONLike:
        """Handler method for the 'offers_made' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.offersMade(var_0).call()
        return {
            'bool': result
        }

