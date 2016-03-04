# coding=utf-8

import time

def parse_time(t):
    if isinstance(t, str):
        try:
            return time.strptime(t, '%Y-%m-%d %H:%M:%S')
        except:
            raise ValueError('Time is not a correct format like yyyy-mm-dd HH:MM:SS')
        
    if isinstance(t, int):
        return time.localtime(t)
    
    if isinstance(t, time.struct_time):
        return t
    
def to_timestamp(t):
    if isinstance(t, str):
        try:
            t = time.strptime(t, '%Y-%m-%d %H:%M:%S')
        except:
            raise ValueError('Time is not a correct format like yyyy-mm-dd HH:MM:SS')
        
    if isinstance(t, time.struct_time):
        return time.mktime(t)
    elif isinstance(t, int):
        return t
    
    return None