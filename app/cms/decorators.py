import functools
from flask import session, redirect, url_for, g
import config


def login_required_(func):
    @functools.wraps(func)
    def decorators(*args, **kwargs):
        # if session.get('user_id'):
        if session.get(config.CMS_USER_ID):
            return func(*args, **kwargs)
        return redirect(url_for('cms.login'))
    return decorators


def permission_required(permission):
    def outter(func):
        @functools.wraps(func)
        def decorator(*args, **kwargs):
            user = g.cms_user
            if user.has_permission(permission):
                return func(*args, **kwargs)
            return redirect(url_for('cms.index'))
        return decorator
    return outter
