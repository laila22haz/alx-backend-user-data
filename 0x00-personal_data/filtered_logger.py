#!/usr/bin/env python3
"""filter log"""
import mysql.connector
import logging
import os
import re
from typing import List


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


def get_db() -> mysql.connector.connection.MySQLConnection:
    """get_db function"""
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")
    return mysql.connector.connect(
        user=username, password=password, host=db_host, database=db_name)


def main() -> None:
    """main function"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    log = get_logger()
    for row in cursor:
        data = []
        for desc, value in zip(cursor.description, row):
            pair = f"{desc[0]}={str(value)}"
            data.append(pair)
        row_str = "; ".join(data)
        log.info(row_str)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
