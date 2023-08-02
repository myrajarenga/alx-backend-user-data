#!/usr/bin/python3
"""
filter_datum using regex
"""
import re
from typing import List
import logging


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""
 
    REDACTION = "***"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super().__init__("[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s")
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        record.msg = filter_datum(self.fields, self.REDACTION, record.msg, self.SEPARATOR)
        return super().format(record)


def filter_datum(
        fields: List[str], redaction: str,
        message: str, separator: str
        ) -> str:
    """function onbfuscate specific fields in log mesage"""
    return re.sub(
            fr'({"|".join(map(re.escape, fields))})=([^{separator}]*)',
            fr'\1={redaction}', message
            )
