from engine.modules.module import Module


class NopEncoding(Module):
    def __init__(self, **kwargs):
        super(NopEncoding, self).__init__(**kwargs)
        self.pretty_name = 'None'

    def run(self, value):
        return value


