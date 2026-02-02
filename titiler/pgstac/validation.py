"""
Validation functions for caller-provided data.
"""

import json
import re

from cql2 import Expr
from pydantic import ValidationError

from titiler.pgstac.model import FilterLang


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


def validate_json(json_str: str | None) -> str | None:
    """
    Verify that a JSON string can be parsed.
    :param json_str: Caller-provided JSON value.
    :type json_str: str | None
    :return: Caller-provided JSON value if validated, otherwise an exception is raised.
    :rtype: str
    """
    if json_str is None:
        return None
    try:
        json.loads(json_str)
    except Exception as e:
        raise ValueError("invalid JSON content") from e
    return json_str


def validate_filter(filter_expr: str | None, filter_lang: FilterLang) -> None:
    """
    Verify that a filter string can be parsed, parsing is determined by the language used.
    :param filter_expr: Caller-provided filter value.
    :type filter_expr: str | None
    :param filter_lang: Caller-provided language value.
    :type filter_lang: str
    """
    if filter_expr is None:
        return
    if filter_lang == "cql2-json":
        try:
            validate_json(json_str=filter_expr)
        except ValueError as e:
            raise ValidationError(str(e), []) from e
    elif filter_lang == "cql2-text":
        try:
            Expr(filter_expr).validate()
        except Exception as e:
            raise ValidationError(str(e), []) from e
