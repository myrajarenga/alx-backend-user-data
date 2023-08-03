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
from os import environ


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Constructor method for RedactingFormatter class

        Args:
            fields: list of fields to redact in log messages
        """
        # Define the format string as a separate variable
        log_format = ("[HOLBERTON] %(name)s %(levelname)s"
                      "%(asctime)-15s: %(message)s")

        # Use the variable in super().__init__()
        super().__init__(log_format)

        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats the specified log record as text.

        Filters values in incoming log records using filter_datum.
        """
        record.msg = filter_datum(
                self.fields, self.REDACTION, record.msg, self.SEPARATOR
                )
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
    """
    Returns a Logger object for handling Personal Data

    Returns:
        A Logger object with INFO log level and RedactingFormatter
        formatter for filtering PII fields
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    pii_fields = ('name', 'email', 'phone', 'ssn', 'password')
    formatter = RedactingFormatter(pii_fields)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger


# # PII fields to be redacted
PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def get_db():
    """
    Returns a MySQLConnection object for accessing Personal Data database

    Returns:
        A MySQLConnection object using connection details from
        environment variables
    """
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
