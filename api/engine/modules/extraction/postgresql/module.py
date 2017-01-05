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
        self.host = self.config["host-port"]
        self.port = self.config["port"]
        self.user = self.config['username']
        self.password = self.config['password']
        self.db = self.config["db"]
        self.table = self.config["table"]

    @staticmethod
    def pretty_name():
        return "PostgreSQL Extractor"

    def run(self):
        # Define our connection string
        conn_string = "host='{}' port='{}' dbname='{}' user='{}' password='{}'".format(self.host, self.port,
                                                                                       self.db, self.user,
                                                                                       self.password)

        # get a connection, if a connect cannot be made an exception will be raised here
        conn = psycopg2.connect(conn_string)

        # conn.cursor will return a cursor object, you can use this cursor to perform queries
        cursor_schema = conn.cursor()
        cursor_schema.execute("select column_name, data_type, character_maximum_length "
                              "from INFORMATION_SCHEMA.COLUMNS where table_name = '{}';"
                              .format(self.table))
        for db_column in cursor_schema:
            self.add_to_schema(Column(db_column[0], type=db_column[1]))

        cursor_rows = conn.cursor()
        cursor_rows.execute("SELECT * FROM \"{}\"".format(self.table))

        for row in cursor_rows:
            # Create new Record
            self.records.append(Record())
            for idx, col_value in enumerate(row):
                column_obj = Column(self.schema[idx].name)
                # Create one field per column
                column_obj.fields.append(self.get_field_from_value(col_value))
                self.records[cursor_rows.rownumber - 1].columns[column_obj.name] = column_obj

        return self.schema, self.records

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
                        'type': 'text'
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
                        'type': 'text'
                    }
                ]
            },
            'db': {
                'label': 'Database',
                'type': 'text'
            },
            'table': {
                'label': 'Table',
                'type': 'text'
            }
        }
