from engine.modules.module import Module


class NopSegmentation(Module):
    """
    Pone output field = columna.name
    """
    def __init__(self, records, **kwargs):
        super(NopSegmentation, self).__init__(**kwargs)
        self.records = records

    @staticmethod
    def pretty_name():
        return "Nop Segmentation"

    def run(self):
        for r in self.records:
            for cname, c in r.columns.items():
                for f in c.fields:
                    f.output_field = ""

        return self.records

