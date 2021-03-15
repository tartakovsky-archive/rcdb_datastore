import re
from typing import Type

from pydantic.types import ConstrainedStr, _registered


def constr_upper(v, field, config):
    upper = field.type_.to_upper or config.anystr_upper
    if upper:
        v = v.upper()
    return v


class ConstrainedStrWithUpper(ConstrainedStr):
    to_upper = False

    @classmethod
    def __get_validators__(cls):
        yield from super().__get_validators__()
        yield constr_upper


def constr(
    *,
    strip_whitespace: bool = False,
    to_lower: bool = False,
    to_upper: bool = False,
    strict: bool = False,
    min_length: int = None,
    max_length: int = None,
    curtail_length: int = None,
    regex: str = None,
) -> Type[str]:
    # use kwargs then define conf in a dict to aid with IDE type hinting
    namespace = dict(
        strip_whitespace=strip_whitespace,
        to_lower=to_lower,
        to_upper=to_upper,
        strict=strict,
        min_length=min_length,
        max_length=max_length,
        curtail_length=curtail_length,
        regex=regex and re.compile(regex),
    )
    return _registered(type('ConstrainedStrWithUpperValue', (ConstrainedStrWithUpper,), namespace))


symbol_type = constr(to_upper=True, max_length=16, min_length=4)
exchange_type = constr(to_upper=True, max_length=16, min_length=2)
