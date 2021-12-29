import sys
import os
import sqlite3


class DbContext:
    # .ctor
    def __init__(self, uri):
        assert uri[-3:] == ".db"
        self.uri = uri
        self.connection = None

        # Если есть схема, подкключиться
        if os.path.isfile(uri):
            self.connection = sqlite3.connect(uri)
        # Если нет, создать
        else:
            os.system(f"sqlite3 {uri}")
            self.connection = sqlite3.connect(uri)

        self.schema = uri[:-3]
        self.path = uri
        self.cursor = self.connection.cursor()
        #self.tables = dict()

    #Создание таблички
    def CreateTable(self, table_name : str, columns : tuple):
        column_str = "(" + ",\n".join([f"{name} {type_s} {' '.join(args)} " for (name, type_s, args) in columns]) + ")"

        query = f"CREATE TABLE IF NOT EXISTS {table_name}\n {column_str};\n"
        self.cursor.execute(query)
        self.connection.commit()

    # Insert Script
    def Insert(self, table_name: str, columns_data : tuple, values: tuple):
        query = f" INSERT INTO {table_name} ({','.join(columns_data)})\n VALUES ({str('?,'*len(values))[:-1]})"
        data_tuple = values
        self.connection.execute(query, data_tuple)
        self.connection.commit()

    def Truncate(self, table_name: str):
        query = f"DELETE FROM {table_name}"
        self.connection.execute(query)
        self.connection.commit()

    def Disconnect(self):
        self.cursor.close()
