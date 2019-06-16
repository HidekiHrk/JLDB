import re
from jldb.interpreter import Interpreter

# util functions #
def set_key(obj, key, value):
    obj[key] = value
    return obj

class Table:
    def __init__(self, client, table_id: str):
        self.client = client
        self.id = table_id

    @property
    def _dict(self):
        return self.client.get_table_dict(self.id)

    @_dict.setter
    def _dict(self, value):
        self.client.update_table(self.id, value)

    @property
    def name(self):
        return self._dict['name']
    
    @property
    def columns(self):
        cols = self._dict['columns']
        return dict(map(lambda x: [x, eval(cols[x])], cols))

    @columns.setter
    def columns(self, value):
        self._dict = set_key(self._dict, 'columns', 
            dict(map(lambda x: [x, value[x].__name__], value)))

    @property
    def d_rows(self):
        return self._dict['rows']

    @d_rows.setter
    def d_rows(self, value):
        self._dict = set_key(self._dict, 'rows', value)

    @property
    def rows(self) -> list:
        return list(map(lambda x: Row(self, x), self.d_rows))
    
    def get_rows(self, **cols):
        if all(x in self.columns for x in list(cols)):
            return list(filter(lambda x:
                len(list(filter(lambda y: getattr(x, y) == cols[y], cols))),self.rows))
        else:
            raise Exception(f'All cols must be {self.name} columns')

    def get_first(self, **cols):
        rws = self.get_rows(**cols)
        return rws[0] if len(rws) else None

    def add_row(self, **cols):
        if all(x in self.columns for x in list(cols)):
            col_id = max(self.d_rows) + 1 if self.d_rows else 0
            self.d_rows = set_key(self.d_rows, col_id,
                dict(map(lambda x: [x, self.columns.get(x)(cols[x])], cols))
            )
            return Row(self, col_id)
        else:
            raise Exception(f'All cols must be {self.name} columns')

class Client(object):
    def __init__(self, filename="data.jldb"):
        self.interpreter = Interpreter(filename=filename)

    def add_table(self, table_name: str, **columns):
        if self.get_table(table_name): return self.get_table(table_name)
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
        return self.get_table(table_name)

    def get_table_dict(self, table_id: str):
        return self.interpreter.read().get(table_id)

    @property
    def tables(self):
        table_dict = self.interpreter.read()
        return list(map(lambda x: Table(self, x), table_dict))

    def get_table(self, table_name: str) -> Table:
        tables = list(filter(lambda x: x.name == table_name, self.tables))
        return tables[0] if tables else None

    def update_table(self, table_id: str, new_dict:dict):
        new_tables_dict = self.interpreter.read()
        new_tables_dict[table_id] = new_dict
        self.interpreter.update(new_tables_dict)

class Row(object):
    def __init__(self, table, row_id: int):
        super().__setattr__('table', table)
        super().__setattr__('row_id', row_id)
        super().__setattr__('_Row__column_types', self.table.columns)

    @property
    def __rowdict(self):
        return self.table.d_rows[self.row_id]

    def __setattr__(self, name, value):
        if self.__rowdict.get(name) != None:
            r_dict = self.__rowdict
            r_dict[name] = self.__column_types[name](value)
            self.table.d_rows = set_key(self.table.d_rows, self.row_id, r_dict)
        else:
            return super().__setattr__(name, value)

    def __getattr__(self, name):
        if self.__rowdict.get(name) != None:
            return self.__rowdict.get(name)

if __name__ == "__main__":
    print("U should close that program huh?")