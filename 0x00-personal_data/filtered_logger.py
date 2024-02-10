#!/usr/bin/env python3
"""filter log"""
import re
from typing import List
import logging


def filter_datum(
        fields: List[str], redaction: str,
        message: str, separator: str) -> str:
    """filter_datum function"""
    for f in fields:
        reg = f"{f}=[^{separator}]*"
        """each field in the ["password", "date_of_birth"] become
        like 'password=' but we exclu the separator with the ^
        like (except ";")
        """
        # print(reg)
        message = re.sub(reg, f"{f}={redaction}", message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """format function"""
        record.message = filter_datum(self.fields, self.REDACTION,
                                      record.message, self.SEPARATOR)
        return super().format(record)


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def get_logger() -> logging.Logger:
    """get_logger function"""
    log = logging.getLogger("user_data")
    log.setLevel(logging.INFO)
    log.propagate = False
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    log.addHandler(console_handler)
    return log
