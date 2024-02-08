#!/usr/bin/env python3
"""filter log"""
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
