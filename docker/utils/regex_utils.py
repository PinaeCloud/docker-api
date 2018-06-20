# coding=utf-8

import re

def parse_line(regex , line):
    if not line:
        return None
    if not regex:
        return line
    
    items = []
    pattern = re.compile(regex)
    match = pattern.match(line)
    if match:
        items = match.groups()
                
    return items

def check_line(regex, line):
    if not line:
        return False
    if not regex:
        return False
    pattern = re.compile(regex)
    match = pattern.match(line)
    if match:
        return True
    else:
        return False
    