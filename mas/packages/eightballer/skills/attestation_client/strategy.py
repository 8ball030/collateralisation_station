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

"""package contains a model for the attestaion behaviour."""

from typing import List, Optional

from aea.skills.base import Model

DEFAULT_ATTESTATION_ENABLED = True
DEFAULT_ATTESTATION_ADDRESSES = ["0x8bA1141B3ebA8205961a29B343aA42178B83C813"]


class AttestationClientModel(Model):
    """class scaffolds a strategy which will allow the handler to reply to attestation requets."""

    attestation_enabled: bool = True
    attestor_addresses: Optional[List[str]] = None

    def __init__(self, **kwargs):
        """Initialize the attestation model."""
        self.attestation_enabled = kwargs.pop("attestation_enabled", True)
        self.attestor_addresses = kwargs.pop(
            "attestor_addresses", DEFAULT_ATTESTATION_ENABLED
        )
        super().__init__(**kwargs)
