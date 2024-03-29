# -*- coding: utf-8 -*-

import warnings


# Global register dict for third party
# template functions, filters and extensions.
_local_env = {
    "globals": {},
    "tests": {},
    "filters": {},
}


def _update_env(env):
    """
    Given a jinja environment, update it with third party
    collected environment extensions.
    """

    env.globals.update(_local_env["globals"])
    env.tests.update(_local_env["tests"])
    env.filters.update(_local_env["filters"])


def _attach_function(attr, func, name=None):
    if name is None:
        name = func.__name__

    global _local_env
    _local_env[attr][name] = func
    return func


def _register_function(attr, name=None, fn=None):
    if name is None and fn is None:
        def dec(func):
            return _attach_function(attr, func)
        return dec

    elif name is not None and fn is None:
        if callable(name):
            return _attach_function(attr, name)
        else:
            def dec(func):
                return _register_function(attr, name, func)
            return dec

    elif name is not None and fn is not None:
        return _attach_function(attr, fn, name)

    raise RuntimeError("Invalid parameters")


def global_function(*args, **kwargs):
    return _register_function("globals", *args, **kwargs)


def test(*args, **kwargs):
    return _register_function("tests", *args, **kwargs)


def filter(*args, **kwargs):
    return _register_function("filters", *args, **kwargs)


class Library(object):
    def __init__(self):
        warnings.warn("Use Library class is deprecated and will be removed "
                      "in future versions", DeprecationWarning, stacklevel=2)

    def global_function(self, *args, **kwargs):
        return _register_function("globals", *args, **kwargs)

    def test(self, *args, **kwargs):
        return _register_function("tests", *args, **kwargs)

    def filter(self, *args, **kwargs):
        return _register_function("filters", *args, **kwargs)

    def __setitem__(self, item, value):
        _env = _get_env()
        _env.globals[item] = value

    def __getitem__(self, item, value):
        _env = _get_env()
        return _env.globals[item]
