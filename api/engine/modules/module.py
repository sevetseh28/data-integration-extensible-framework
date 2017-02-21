class Module(object):
    config_json = {}

    def __init__(self, **kwargs):
        if "config" in kwargs:
            config = kwargs["config"]
        else:
            config = {}
        self.config = config

    @staticmethod
    def pretty_name():
        return "Generic Module"

    @staticmethod
    def config_json(**kwargs):
        return {}
