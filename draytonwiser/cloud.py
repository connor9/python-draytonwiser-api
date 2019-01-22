from .wiserapi import WiserBaseAPI

class Cloud(WiserBaseAPI):
    def __init__(self, *args, **kwargs):
        # Defining default values

        self.environment = None # "Prod",
        self.detailed_publishing = None # false,
        self.wiser_api_host = None # "api-nl.wiserair.com",
        self.boot_strap_api_host = None # "bootstrap.gl.struxurewarecloud.com"

        super(Cloud, self).__init__(*args, **kwargs)


