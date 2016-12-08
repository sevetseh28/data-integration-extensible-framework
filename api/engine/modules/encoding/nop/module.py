from engine.modules.module import Module


class NopEncoding(Module):
    def __init__(self, **kwargs):
        super(NopEncoding, self).__init__(**kwargs)
        self.pretty_name = 'None'

    def run(self, value):
        return value

    @staticmethod
    def pretty_name():
        return "No encoding"

    @staticmethod
    def config_json(**kwargs):
        return {
            'name': {
                'type': 'hidden',
                'value': 'nop',
            }
        }
