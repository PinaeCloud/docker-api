# coding=utf-8

from text import string_utils as str_utils

def check_container(func):
    def wrapper(*args, **kwargs):
        if str_utils.is_empty(args[1]) and str_utils.is_empty(kwargs.get('container_id')):
                raise ValueError('Container id is Empty')
        return func( *args , **kwargs)
    return wrapper

def check_image(func):
    def wrapper(*args, **kwargs):
        if str_utils.is_empty(args[1]) and str_utils.is_empty(kwargs.get('image_name')):
            raise ValueError('Image name is Empty')
        return func( *args , **kwargs)
    return wrapper