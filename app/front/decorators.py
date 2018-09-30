import functools
from flask import session, redirect, url_for, g
import config


def login_required_(func):
    @functools.wraps(func)
    def decorators(*args, **kwargs):
        # if session.get('user_id'):
        if session.get(config.FRONT_USER_ID):
            return func(*args, **kwargs)
        return redirect(url_for('front.signin'))
    return decorators