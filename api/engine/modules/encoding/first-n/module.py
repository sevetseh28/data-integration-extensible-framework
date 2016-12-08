from engine.modules.module import Module


class FirstNEncoding(Module):
    def __init__(self, config, **kwargs):
        super(FirstNEncoding, self).__init__(**kwargs)
        self.pretty_name = 'None'
        self.first_n = config['first_n']

    def run(self, value):
        return str(value)[0:self.first_n]

    @staticmethod
    def pretty_name():
        return "First-n chars"

    @staticmethod
    def config_json(**kwargs):
        return {
            'name': {
                'type': 'hidden',
                'value': 'first-n',
            },
            'first_n': {
                "type": "slider",
                "label": "Value of N",
                "value": 2,
                "start": 1,
                "end": 10,
                "step": 1,
                "color": "red"
            }
        }
