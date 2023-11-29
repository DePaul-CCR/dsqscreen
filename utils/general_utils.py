from flask import session
from flask import request

def get_score(item_name):
    return int(session[item_name])

def get_client_ip():
    print("--------------------------------------------------------------------------------------------------------")
    print(request.environ)
    print("--------------------------------------------------------------------------------------------------------")
    print(request)
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        return request.environ['REMOTE_ADDR']
    else:
         # if behind a proxy
        return request.environ['HTTP_X_FORWARDED_FOR']