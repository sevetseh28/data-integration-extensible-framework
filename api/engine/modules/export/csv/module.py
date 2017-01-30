import uuid

from engine.models.record import *
from engine.modules.export.export_module import ExportModule
from engine.modules.module import Module
from engine.utils import dynamic_loading
import csv
class CSVExport(ExportModule):
    """
    Formato config:
    {
        'name': "[name]",
    }
    """

    def __init__(self, records,schema, **kwargs):
        super(CSVExport,self).__init__(**kwargs)
        self.records = records
        self.schema = schema
        self.name = self.config["name"] if "name" in self.config and self.config["name"] else 'csv.csv'
        self.delimiter = self.config['delimiter'].__str__()[0] if 'delimiter' in self.config and self.config[
            'delimiter'] else ','

    @staticmethod
    def pretty_name():
        return "CSV"

    def run(self):
        filename = uuid.uuid4()

        with open('files-to-download/{}.csv'.format(filename),'w') as csvfile:
            columnnames = [column['name'] for column in self.schema]
            writer = csv.DictWriter(csvfile,columnnames,restval="NULL",extrasaction="ignore",delimiter=self.delimiter, skipinitialspace=True, quoting=csv.QUOTE_MINIMAL)
            writer.writeheader()
            for record in self.records:
                row = {}
                for column in columnnames:
                    row[column] = record.get_field_col(column)
                writer.writerow(row)






    @staticmethod
    def config_json(**kwargs):
        return {
            'name': {
                'label': 'Name of file',
                'type': 'text'
            },
            'delimiter': {
                'label': 'Delimiter (default: ",")',
                'type': 'text'
            }
        }




