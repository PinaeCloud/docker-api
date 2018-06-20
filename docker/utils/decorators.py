# coding=utf-8

import string_utils

def check_container(func):
    def wrapper(*args, **kwargs):
        if string_utils.is_empty(args[1]) and string_utils.is_empty(kwargs.get('container_id')):
                raise ValueError('Container id is Empty')
        return func( *args , **kwargs)
    return wrapper

def check_image(func):
    def wrapper(*args, **kwargs):
        if string_utils.is_empty(args[1]) and string_utils.is_empty(kwargs.get('image_name')):
            raise ValueError('Image name is Empty')
        return func( *args , **kwargs)
    return wrapper