#!/usr/bin/python3
"""
filter_datum using regex
"""
import re
from typing import List
import logging
import csv
import os
import mysql.connector


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


def get_logger():
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    pii_fields = ('name', 'email', 'phone', 'ssn', 'password')
    formatter = RedactingFormatter(pii_fields)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')

def get_db():
    db_username = os.environ.get('PERSONAL_DATA_DB_USERNAME', 'root')
    db_password = os.environ.get('PERSONAL_DATA_DB_PASSWORD', '')
    db_host = os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.environ.get('PERSONAL_DATA_DB_NAME')

    try:
        db_connection = mysql.connector.connect(
            host=db_host,
            user=db_username,
            password=db_password,
            database=db_name
        )
        return db_connection
    except mysql.connector.Error as e:
        print(f"Error connecting to the database: {e}")
        return None
