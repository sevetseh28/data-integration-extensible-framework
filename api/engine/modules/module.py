class Module(object):
    required_config = {}

    def __init__(self, config=None):
        if config is None:
            config = {}
        self.config = config

    @staticmethod
    def pretty_name():
        return "Generic Module"

    @staticmethod
    def required_config():
        return {}
