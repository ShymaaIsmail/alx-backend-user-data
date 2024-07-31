#!/usr/bin/env python3
"""Filter Logger"""
import re


def filter_datum(fields, redaction, message, separator):
    """Mask value of fileds with xxxx"""
    pattern = f"({'|'.join(map(re.escape, fields))})=.+?({separator}|$)"
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}{m.group(2)}", message)
