"""
Validation functions for caller-provided data.
"""

import json
import re


def validate_datetime(datetime_value: str) -> str:
    """
    Verify that a datetime string matches one accepted regex pattern.
    :param datetime_value: Caller-provided datetime value.
    :type datetime_value: str
    :return: Caller-provided datetime value if validated, otherwise an exception is raised.
    :rtype: str
    """
    single_pattern = (
        r"((?:(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}:\d{2}(?:\.\d+)?))(Z|[\+-]\d{2}:\d{2})?)"
    )
    if (
        re.match(f"^{single_pattern}$", datetime_value)
        or re.match(rf"^\.\./{single_pattern}$", datetime_value)
        or re.match(rf"^{single_pattern}/\.\.$", datetime_value)
        or re.match(f"{single_pattern}/{single_pattern}", datetime_value)
    ):
        return datetime_value
    raise ValueError("value does match a supported pattern")


def validate_json_structure(json_str: str) -> str:
    """
    Verify that a string parameter provides valid JSON.
    :param json_str: Caller-provided JSON string
    :type json_str: str
    :return: Caller-provided JSON string if validated, otherwise an exception is raised.
    :rtype: str
    """
    try:
        json.loads(json_str)
    except Exception as e:
        raise ValueError("invalid JSON content") from e
    return json_str
