#!/usr/bin/python3
"""
filter_datum using regex
"""
import re
from typing import List


def filter_datum(
        fields: List[str], redaction: str,
        message: str, separator: str
        ) -> str:
    """function onbfuscate specific fields in log mesage"""
    return re.sub(
            fr'({"|".join(map(re.escape, fields))})=([^{separator}]*)',
            fr'\1={redaction}', message
            )
