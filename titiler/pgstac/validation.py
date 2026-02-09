"""
Validation functions for caller-provided data.
"""

import re

from cql2 import Expr
from pydantic import ValidationError

from titiler.core.validation import validate_json
from titiler.pgstac.model import FilterLang


def validate_datetime(datetime_value: str) -> str:
    """
    Verify that a datetime string matches one accepted regex pattern.
    :param datetime_value: Caller-provided datetime value.
    :type datetime_value: str
    :return: Caller-provided datetime value if validated, otherwise an exception is raised.
    :rtype: str
    """
    single_datetime_regex = (
        r"((?:(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}:\d{2}(?:\.\d+)?))(Z|[\+-]\d{2}:\d{2})?)"
    )
    if (
        re.match(f"^{single_datetime_regex}$", datetime_value)
        or re.match(rf"^\.\./{single_datetime_regex}$", datetime_value)
        or re.match(rf"^{single_datetime_regex}/\.\.$", datetime_value)
        or re.match(f"{single_datetime_regex}/{single_datetime_regex}", datetime_value)
    ):
        return datetime_value
    raise ValueError("invalid datetime format")


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


def validate_bbox(bbox_str: str | None) -> str | None:
    """
    Verify that a BBOX string can be parsed.
    :param bbox_str: Caller-provided bbox value.
    :type bbox_str: str | None
    :return: Caller-provided bbox value if validated, otherwise an exception is raised.
    :rtype: str

    """
    if bbox_str is None:
        return None
    parseable_float_regex = r"\s*(-)?\d+((\.\d+)(e\d+)?)?\s*"  # can simply call titiler.core.validation.validate_bbox on titiler.core > 1.1.1 when released
    if re.match(
        "^{}$".format(",".join([parseable_float_regex for _ in range(4)])), bbox_str
    ) or re.match(
        "^{}$".format(",".join([parseable_float_regex for _ in range(6)])), bbox_str
    ):
        return bbox_str
    raise ValueError("invalid bbox content")
