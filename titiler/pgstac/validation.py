"""
Validation functions for caller-provided data.
"""

import re
from typing import Literal

from cql2 import Expr
from pydantic import ValidationError

from titiler.core.validation import validate_json


def validate_filter(
    filter_expr: str | None, filter_lang: Literal["cql2-text", "cql2-json"]
) -> None:
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
