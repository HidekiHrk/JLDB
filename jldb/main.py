import re
from jldb.interpreter import Interpreter

class Client(object):
    def __init__(self, filename="data.jldb"):
        self.interpreter = Interpreter(filename=filename)

    def add_table(self, table_name: str, **columns):
        if self.get_table(table_name): return
        tables = self.interpreter.read()
        tables_last_id = list(tables)[-1] if len(tables) else None
        new_id = int(tables_last_id[len("table_"):]) + 1 if tables_last_id else 0
        table_dict = {
            "name":table_name,
            "columns": dict(map(lambda x: [x, columns[x].__name__], columns)),
            "rows":{}
        }
        tables[f'table_{new_id}'] = table_dict
        self.interpreter.update(tables)

    def get_table_dict(self, table_id: str):
        return self.interpreter.read().get(table_id)

    @property
    def tables(self):
        table_dict = self.interpreter.read()
        return list(map(lambda x: Table(self, x), table_dict))

    def get_table(self, table_name: str):
        tables = list(filter(lambda x: x.name == table_name, self.tables))
        return tables[0] if tables else None

class Table:
    def __init__(self, client: Client, table_id: str):
        self.client = client
        self.id = table_id
    
    @property
    def _dict(self):
        return self.client.get_table_dict(self.id)

    @property
    def name(self):
        return self._dict['name']
    
    @property
    def columns(self):
        cols = self._dict[columns]
        return dict(map(lambda x: [x, eval(cols[x])], cols))

    @property
    def __rows(self):
        return self._dict['rows']

    @property
    def rows(self):
        return list(self.__rows)

    def add_row(self, **kwargs):


class Row(object):
    def __init__(self, table: Table, row_id: int):
        pass
        