from flask import session

def get_score(item_name):
    return int(session[item_name])