import base64
import sys
import os
import sqlite3
import psutil
import requests


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
        # self.tables = dict()

    # Создание таблички
    def CreateTable(self, table_name: str, columns: tuple):
        column_str = "(" + ",\n".join([f"{name} {type_s} {' '.join(args)} " for (name, type_s, args) in columns]) + ")"

        query = f"CREATE TABLE IF NOT EXISTS {table_name}\n {column_str};\n"
        self.cursor.execute(query)
        self.connection.commit()

    # Insert Script
    def Insert(self, table_name: str, columns_data: tuple, values: tuple, download=False):
        if download:
            download_if_needed(columns_data, values)

        query = f" INSERT INTO {table_name} ({','.join(columns_data)})\n VALUES ({str('?,' * len(values))[:-1]})"
        data_tuple = values

        self.connection.execute(query, data_tuple)
        self.connection.commit()

    # select on predicate
    def Select(self, table_name, predicate="1=1", columns=None):
        col_str = ','.join(columns) if (columns is not None and len(columns) > 0) else '*'
        query = f"SELECT {col_str} FROM {table_name} WHERE {predicate}"
        res = self.connection.execute(query).fetchall()
        return res

    # delete on predicate
    def Update(self, table_name, columns: list, values: list, predicate="1=1", download=False):
        if download:
            download_if_needed(columns, values)

        update_str = "SET " + ",".join([f"{field} = {value}" for field, value in zip(columns, values)])
        query = f"UPDATE {table_name} {update_str} WHERE {predicate}"
        self.connection.execute(query)
        self.connection.commit()

    def Disconnect(self):
        self.cursor.close()

    def Delete(self, table_name, predicate="1=1"):
        if predicate == '':
            return

        query = f"DELETE FROM {table_name} WHERE {predicate}"
        self.connection.execute(query)
        self.connection.commit()


def download_if_needed(columns: list, values: list):
    if "base64" in columns and "src" in "columns":
        src_idx = columns.index("src")
        b64_idx = columns.index("base64")

        response = requests.get(columns[src_idx])
        b64img = base64.b64encode(response.content)
        values[b64_idx] = b64img
