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

    def __init__(self, matches, non_matches, schema, **kwargs):
        super(CSVExport,self).__init__(**kwargs)
        self.matches = matches
        self.non_matches = non_matches
        self.only_matches = self.config['only_matches']['checked'] if "only_matches" in self.config and \
                                                                      self.config["only_matches"] else False
        self.schema = schema
        self.name = self.config["name"] if "name" in self.config and self.config["name"] else 'csv.csv'
        self.delimiter = self.config['delimiter'].__str__()[0] if 'delimiter' in self.config and self.config[
            'delimiter'] else ','

    @staticmethod
    def pretty_name():
        return "CSV"

    def run(self):
        self.records = self.matches

        if not self.only_matches:
            self.records += self.non_matches

        filename = uuid.uuid4()

        with open('files-to-download/{}.csv'.format(filename),'wb') as csvfile:
            columnnames = [column['custom_name'] if column['custom_name'] is not None else column['name'] for column in self.schema]
            col_name_map = {(col['custom_name'] if col['custom_name'] is not None else col['name']): col['name'] for col in self.schema}

            writer = csv.DictWriter(csvfile,columnnames,restval="NULL",extrasaction="ignore",delimiter=self.delimiter, skipinitialspace=True, quoting=csv.QUOTE_MINIMAL)
            writer.writeheader()
            for record in self.records:
                row = {}
                for column in columnnames:
                    row[column] = record.get_field_col(col_name_map[column])
                writer.writerow(row)
        return self.name,str(filename)+'.csv'





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
            },
            'only_matches': {
                'label': 'Export only matches',
                'type': 'toggleswitch',
                "color": 'blue',
                'checked': False
            },
        }




