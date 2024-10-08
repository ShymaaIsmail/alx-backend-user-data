#!/usr/bin/env python3
"""Filter Logger"""
import datetime
import os
import re
import logging
from typing import List, Tuple
import mysql.connector


PII_FIELDS: Tuple[str, ...] = ("name", "email", "phone", "ssn", "password")


def get_logger() -> logging.Logger:
    """Creates and returns a logger named 'user_data'"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Mask value of fields with redaction"""
    pattern = f"({'|'.join(map(re.escape, fields))})=.+?({separator}|$)"
    return re.sub(pattern,
                  lambda m: f"{m.group(1)}={redaction}{m.group(2)}", message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """initiator function"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format logger using class fields property """
        original_message = super().format(record)
        return filter_datum(self.fields, self.REDACTION,
                            original_message, self.SEPARATOR)


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ Connection to MySQL environment """
    db_connect = mysql.connector.connect(
        user=os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=os.getenv('PERSONAL_DATA_DB_PASSWORD', ''),
        host=os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        database=os.getenv('PERSONAL_DATA_DB_NAME')
    )
    return db_connect


def main():
    """Main function to retrieve and display user data."""
    db = get_db()
    if db:
        cursor = db.cursor()
        cursor.execute("SELECT name, email, phone, ssn,\
                        password, ip, last_login, user_agent FROM users;")
        rows = cursor.fetchall()

        for row in rows:
            ip, last_login, user_agent = row
            # Display the filtered data
            print(f"[HOLBERTON] user_data INFO {datetime.datetime.now()}: "
                  f"name=***; email=***; phone=***; ssn=***; password=***; "
                  f"ip={ip}; last_login={last_login}; user_agent={user_agent};"
                  )

        cursor.close()
        db.close()


if __name__ == "__main__":
    main()
