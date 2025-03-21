"""
Copyright (c) Microsoft Corporation. All rights reserved.
Licensed under the MIT License.
"""

from __future__ import annotations

import json
from typing import Any

import yaml

from ..ai.tokenizers import Tokenizer
from ..state import todict


def to_string(tokenizer: Tokenizer, value: Any, as_json: bool = False) -> str:
    """
    Converts a value to a string representation.
    Dates are converted to ISO strings and Objects are converted to JSON or YAML,
    whichever is shorter.

    Args:
        tokenizer (Tokenizer): The tokenizer object used for encoding.
        value (Any): The value to be converted.
        as_json (bool, optional): Flag indicating whether to return the value as JSON string.
        Defaults to False.

    Returns:
        str: The string representation of the value.
    """
    if value is None:
        return ""

    if hasattr(value, "isoformat") and callable(value.isoformat):
        # Used when the value is a datetime object
        return value.isoformat()
    value = todict(value)

    if as_json:
        return json.dumps(value, default=lambda o: o.__dict__, ensure_ascii=False)

    # Return shorter version of object
    yaml_str = yaml.dump(value, allow_unicode=True)
    json_str = json.dumps(value, default=lambda o: o.__dict__, ensure_ascii=False)
    if len(tokenizer.encode(yaml_str)) < len(tokenizer.encode(json_str)):
        return yaml_str

    return json_str
