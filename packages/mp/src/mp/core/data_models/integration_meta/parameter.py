# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

import dataclasses
from typing import NotRequired

import mp.core.data_models.abc
import mp.core.utils
from mp.core.data_models.script.parameter import ScriptParamType


class BuiltIntegrationParameter(mp.core.data_models.abc.BaseBuiltTypedDict):
    PropertyName: str
    PropertyDisplayName: str
    Value: str | bool | float | int | None
    PropertyDescription: str
    IsMandatory: bool
    PropertyType: int
    IntegrationIdentifier: str


class NonBuiltIntegrationParameter(mp.core.data_models.abc.BaseNonBuiltTypedDict):
    name: str
    value: NotRequired[str | bool | float | int]
    description: str
    is_mandatory: bool
    type: str
    integration_identifier: str


@dataclasses.dataclass(slots=True, frozen=True)
class IntegrationParameter(
    mp.core.data_models.abc.Buildable[
        BuiltIntegrationParameter,
        NonBuiltIntegrationParameter,
    ],
):
    name: str
    description: str
    is_mandatory: bool
    type_: ScriptParamType
    integration_identifier: str
    default_value: str | bool | float | int | None

    @classmethod
    def _from_built(cls, built: BuiltIntegrationParameter) -> IntegrationParameter:
        return cls(
            name=built["PropertyName"],
            default_value=built["Value"],
            description=built["PropertyDescription"],
            is_mandatory=built["IsMandatory"],
            type_=ScriptParamType(int(built["PropertyType"])),
            integration_identifier=built["IntegrationIdentifier"],
        )

    @classmethod
    def _from_non_built(
        cls,
        non_built: NonBuiltIntegrationParameter,
    ) -> IntegrationParameter:
        return cls(
            name=non_built["name"],
            default_value=non_built.get("value"),
            description=non_built["description"],
            is_mandatory=non_built["is_mandatory"],
            type_=ScriptParamType.from_string(non_built["type"]),
            integration_identifier=non_built["integration_identifier"],
        )

    def to_built(self) -> BuiltIntegrationParameter:
        """Turn the object into a `BuiltIntegrationParameter`.

        Returns:
            The "built" representation of the object.

        """
        return {
            "IntegrationIdentifier": self.integration_identifier,
            "IsMandatory": self.is_mandatory,
            "PropertyDescription": self.description,
            "PropertyDisplayName": self.name,
            "PropertyName": self.name,
            "PropertyType": self.type_.value,
            "Value": self.default_value,
        }

    def to_non_built(self) -> NonBuiltIntegrationParameter:
        """Turn the object into a `NonBuiltIntegrationParameter`.

        Returns:
            The "non-built" representation of the object.

        """
        return mp.core.utils.copy_mapping_without_none_values(  # type: ignore[return-value]
            {
                "name": self.name,
                "value": self.default_value,
                "type": self.type_.to_string(),
                "description": self.description,
                "is_mandatory": self.is_mandatory,
                "integration_identifier": self.integration_identifier,
            },
        )
