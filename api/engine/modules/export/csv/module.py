from engine.models.record import *
from engine.modules.export.export_module import ExportModule
import csv
class CSVExport(ExportModule):
    """
    Formato config:
    {
        'name': "[name]",
    }
    """

    def __init__(self, records,schema, **kwargs):
        super(CSVExport,self)._init_init(**kwargs)
        self.records = records
        self.schema = schema
        self.name = self.config["name"] if "host" in self.config and self.config["host"] else 'csv.csv'

    @staticmethod
    def pretty_name():
        return "CSVExport"

    def run(self):
        pass

    @staticmethod
    def config_json(**kwargs):
        return {
            'name': {
                'label': 'Name of file',
                'type': 'text'
            }
        }




