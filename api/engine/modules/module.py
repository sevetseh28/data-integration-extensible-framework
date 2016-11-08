class Module(object):
    config_json = {}

    def __init__(self, config=None):
        if config is None:
            config = {}
        self.config = config

    @staticmethod
    def pretty_name():
        return "Generic Module"

    @staticmethod
    def config_json(**kwargs):
        return {}
