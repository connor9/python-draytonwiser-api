# -*- coding: utf-8 -*-

from .wiserapi import WiserBaseAPI

class Cloud(WiserBaseAPI):
    """Represnts the /Cloud object in the Restful API"""


    def __init__(self, *args, **kwargs):
        self.environment = None # "Prod",
        self.detailed_publishing = None # false,
        self.wiser_api_host = None # "api-nl.wiserair.com",
        self.boot_strap_api_host = None # "bootstrap.gl.struxurewarecloud.com"

        super(Cloud, self).__init__(*args, **kwargs)