import csv
import uuid

from engine.modules.export.export_module import ExportModule


class CSVExport(ExportModule):
    """
    Formato config:
    {
        'name': "[name]",
    }
    """

    def __init__(self, records, schema, **kwargs):
        super(CSVExport, self).__init__(**kwargs)
        self.records = records
        self.only_matches = self.config['only_matches']['checked'] if "only_matches" in self.config and \
                                                                      self.config["only_matches"] else False
        self.schema = schema
        self.name = self.config["1_name"] if "1_name" in self.config and self.config["1_name"] else 'csv.csv'
        self.delimiter = self.config["2_delimiter"].__str__()[0] if "2_delimiter" in self.config and self.config[
            "2_delimiter"] else ','

    @staticmethod
    def pretty_name():
        return "CSV"

    def run(self):
        filename = uuid.uuid4()

        with open(f'{filename}.csv', 'w+', encoding='utf-8') as csvfile:
            columnnames = [column['custom_name'] if column['custom_name'] is not None else column['name'] for column in
                           self.schema]
            col_name_map = {(col['custom_name'] if col['custom_name'] is not None else col['name']): col['name'] for col
                            in self.schema}

            writer = csv.DictWriter(csvfile, columnnames, restval="NULL", extrasaction="ignore",
                                    delimiter=self.delimiter, skipinitialspace=True, quoting=csv.QUOTE_MINIMAL)
            writer.writeheader()
            for record in self.records:
                row = {}
                for column in columnnames:
                    row[column] = record.get_field_col(col_name_map[column])
                writer.writerow(row)
        return self.name, str(filename) + '.csv'

    @staticmethod
    def config_json(**kwargs):
        return {
            '1_name': {
                'label': 'Name of file',
                'type': 'text'
            },
            '2_delimiter': {
                'label': 'Delimiter (default: ",")',
                'type': 'text'
            }
        }
