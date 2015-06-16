# coding=utf-8

def check_version(fn):
    def wrapper(*argv, **kwgs):
        try:
            fun_module = fn.__module__
            fun_name = fn.__name__
            return fn(*argv, **kwgs)
        except Exception, e:
            raise e
    return wrapper

def __get_version_ctrl():
    pass