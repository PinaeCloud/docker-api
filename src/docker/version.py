# coding=utf-8

def check_version(fn):
    def wrapper(*argv, **kwgs):
        try:
            print 'hello'
            return fn(*argv, **kwgs)
        except Exception, e:
            raise e
    return wrapper

def get_version(session):
    url = session._url('/version')
    response = session._result(session._get(url))
    return response