#!/usr/bin/env python3
"""Filter Logger"""
import re
import logging


def filter_datum(fields, redaction, message, separator):
    """Mask value of fields with xxxx"""
    pattern = f"({'|'.join(map(re.escape, fields))})=.+?({separator}|$)"
    return re.sub(pattern,
                  lambda m: f"{m.group(1)}={redaction}{m.group(2)}", message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        filter_datum(self.fields, self.REDACTION,
                     super().format(record), self.SEPARATOR)
