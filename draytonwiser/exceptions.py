# -*- coding: utf-8 -*-
class APIException(Exception):
    """Base exception class for this module"""
    pass

class ObjectNotFoundException(Exception):
    """Base exception class for this module"""
    pass

class HotWaterNotSupportedException(Exception):
    """Base exception class for this module"""
    pass