"""
Validation functions for caller-provided data.
"""

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
