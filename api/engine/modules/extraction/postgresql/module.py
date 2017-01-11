# coding=utf-8
from engine.models.record import *
from engine.modules.extraction.extraction_module import ExtractionModule
from engine.modules.module import Module
import psycopg2
from datetime import datetime
from copy import deepcopy
from unidecode import unidecode


class PostgreSQLExtractor(ExtractionModule):
    """
        Config format:
        {
            'host': "[host]",
            'port': "[port]",
            'user': "[user]",
            'password': "[password]"
            'db': "[db]",
            'table': "[table_name]",
        }
    """

    def __init__(self, **kwargs):
        super(PostgreSQLExtractor, self).__init__(**kwargs)
        self.pretty_name = 'PostgreSQL Extractor'
        self.host = self.config['host-port']['0']
        self.port = self.config['host-port']['1']
        self.user = self.config['auth']['0']
        self.password = self.config['auth']['1']
        self.db = self.config["db-table"]['0']
        self.table = self.config["db-table"]['1']
        self.limit = self.config["db-table"]['2']

    @staticmethod
    def pretty_name():
        return "PostgreSQL Extractor"

    def run(self):
        # Define our connection string
        conn_string = "host='{}' port='{}' dbname='{}' user='{}' password='{}'".format(self.host, self.port,
                                                                                       self.db, self.user,
                                                                                       self.password)

        # get a connection, if a connect cannot be made an exception will be raised here
        try:
            with psycopg2.connect(conn_string) as conn:
                # conn.cursor will return a cursor object, you can use this cursor to perform queries
                cursor_schema = conn.cursor()
                cursor_schema.execute("select column_name, data_type, character_maximum_length "
                                      "from INFORMATION_SCHEMA.COLUMNS where table_name = '{}';"
                                      .format(self.table))
                for db_column in cursor_schema:
                    self.add_to_schema(Column(db_column[0]))

                cursor_rows = conn.cursor()
                query = "SELECT * FROM \"{}\"".format(self.table) if self.limit is '' else \
                    "SELECT * FROM \"{}\" LIMIT {}".format(self.table, self.limit)

                cursor_rows.execute(query)

                for row in cursor_rows:
                    # Create new Record
                    self.records.append(Record())
                    for idx, col_value in enumerate(row):
                        column_obj = Column(self.schema[idx].name)
                        # Create one field per column
                        new_field = self.get_field_from_value(col_value)
                        column_obj.fields.append(new_field)
                        self.records[cursor_rows.rownumber - 1].columns[column_obj.name] = column_obj

                return self.schema, self.records
        except Exception as e:
            raise

    @staticmethod
    def config_json(**kwargs):
        return {

            'host-port': {
                'type': 'row',
                'cols': [
                    {
                        'label': 'Host',
                        'type': 'text'
                    },
                    {
                        'label': 'Port',
                        'type': 'number'
                    }
                ]
            },
            'auth': {
                'type': 'row',
                'cols': [
                    {
                        'label': 'User',
                        'type': 'text'
                    },
                    {
                        'label': 'Password',
                        'type': 'password'
                    }
                ]
            },
            'db-table': {
                'type': 'row',
                'cols': [
                    {
                        'label': 'Database',
                        'type': 'text'
                    },
                    {
                        'label': 'Table',
                        'type': 'text'
                    },
                    {
                        'label': 'Limit',
                        'type': 'number'
                    }
                ]
            }
        }
