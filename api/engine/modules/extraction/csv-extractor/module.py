
from engine.models.record import *
from engine.modules.extraction.extraction_module import ExtractionModule
from engine.modules.module import Module
import csv

class CsvExtractor(ExtractionModule):

    """
        Formato config:
        {
            'pathcsv': "[host]"

        }
    """

    def __init__(self, **kwargs):
        super(CsvExtractor, self).__init__(**kwargs)
        self.pretty_name = 'CsvExtractor'
        self.pathcsv = self.config['pathcsv']
        self.delimiter = self.config['delimiter'].__str__()[0] if 'delimiter' in self.config and self.config['delimiter'] else ','

    @staticmethod
    def pretty_name():
        return "CSV Extractor"

    def run(self):

        with open(self.pathcsv) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=self.delimiter, skipinitialspace=True, quoting=csv.QUOTE_MINIMAL)
            for fieldname in reader.fieldnames:
                self.add_to_schema(Column(fieldname))
            for i,row in enumerate(reader):
                self.records.append(Record())
                for key,value in row.items():
                    column = Column(key)
                    column.fields.append(get_field_from_csv(value))
                    self.records[i].columns[column.name] = column
        return self.schema, self.records

    @staticmethod
    def config_json(**kwargs):
        return {
            'pathcsv': {
                'label': 'CSV',
                'type': 'file'
            },
            'delimiter': {
                'label': 'Delimiter (default: ",")',
                'type': 'text'
            }
        }





def ignore_exception(IgnoreException=Exception,DefaultVal=None):
    def dec(function):
        def _dec(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except IgnoreException:
                return DefaultVal
        return _dec
    return dec


def get_field_from_csv(value):
        return Field(value, EnumType.string)

