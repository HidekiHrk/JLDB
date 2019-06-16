import re
import sys
from jldb.interpreter import Interpreter

# util functions #
def set_key(obj, key, value):
    obj[key] = value
    return obj

def update_dict(obj, ndict):
    obj.__dict__.update(ndict)
    return obj

def get_attr(obj, name, default=None):
    try:
        return getattr(obj, name)
    except AttributeError:
        return default

# Gets a str that indicates a class of a specific module
def get_class_modules_str(obj):
    return f"{obj.__module__}.{obj.__qualname__}"

# Gets a class from the get_class_modules_str function return str
def get_class_modules_from_str(cstr: str):
    cstr = cstr.split('.')
    module = sys.modules[cstr[0]]
    class_names = cstr[1:]
    actual_class = getattr(module, class_names[0])
    for m in class_names[1:]:
        actual_class = getattr(module, class_names[m])
    return actual_class

def instantiate(iclass):
    return iclass.__new__(iclass)

def c_confirm(iclass, value, raw=True):
    iobj = instantiate(iclass)
    if isinstance(get_attr(iobj, '__dict__'), dict):
        return value if raw else update_dict(iobj, value)
    return iclass(value)

class Table:
    def __init__(self, client, table_id: str):
        self.client = client
        self.id = table_id

    @property
    def _dict(self):
        # A function that returns a full dict of current table
        return self.client.get_table_dict(self.id)

    @_dict.setter
    def _dict(self, value):
        # Update the dict to database
        self.client.update_table(self.id, value)

    @property
    def name(self):
        # Database Name
        return self._dict['name']
    
    @property
    def columns(self):
        # Get database columns and types of each one
        cols = self._dict['columns']
        return dict(map(lambda x: [x, get_class_modules_from_str(cols[x])], cols))

    @columns.setter
    def columns(self, value):
        # Update columns key of table dict
        self._dict = set_key(self._dict, 'columns', 
            dict(map(lambda x: [x, get_class_modules_str(value[x])], value)))

    @property
    def d_rows(self):
        # returns a dict of all rows stored in this table
        return self._dict['rows']

    @d_rows.setter
    def d_rows(self, value):
        # updates the rows key of current table dict 
        self._dict = set_key(self._dict, 'rows', value)

    @property
    def rows(self) -> list:
        # Get a list of Row objects that's stored on this table
        return list(map(lambda x: Row(self, x), self.d_rows))
    
    def get_rows(self, **cols):
        # Get a list of rows that matches with the cols
        if all(x in self.columns for x in list(cols)):
            return list(filter(lambda x:
                len(list(filter(lambda y: getattr(x, y) == cols[y], cols))),self.rows))
        else:
            raise Exception(f'All cols must be {self.name} columns')

    def get_first(self, **cols):
        # get the first element that matches with the cols
        rws = self.get_rows(**cols)
        return rws[0] if len(rws) else None

    def add_row(self, **cols):
        # add a row based on cols, each row is unique and have a specific row_id
        if all(x in self.columns for x in list(cols)):
            col_id = max(self.d_rows) + 1 if self.d_rows else 0
            self.d_rows = set_key(self.d_rows, col_id,
                dict(map(lambda x:
                    [x, c_confirm(self.columns.get(x), cols[x])],
                cols))
            )
            return Row(self, col_id)
        else:
            raise Exception(f'All cols must be {self.name} columns')

class Client(object):
    def __init__(self, filename="data.jldb"):
        self.interpreter = Interpreter(filename=filename)

    def add_table(self, table_name: str, **columns):
        """
            add a table with a unique table_name and columns with their respective types
            It's highly recommended to use built-in types
            in case of using other classes as column type, the database should be used
            on the same code, and the other class must have a __dict__ property.
        """
        if self.get_table(table_name): return self.get_table(table_name)
        tables = self.interpreter.read()
        tables_last_id = list(tables)[-1] if len(tables) else None
        new_id = int(tables_last_id[len("table_"):]) + 1 if tables_last_id else 0
        table_dict = {
            "name":table_name,
            "columns": dict(map(lambda x: [x, get_class_modules_str(columns[x])], columns)),
            "rows":{}
        }
        tables[f'table_{new_id}'] = table_dict
        self.interpreter.update(tables)
        return self.get_table(table_name)

    def get_table_dict(self, table_id: str):
        # Gets a dict for this table
        return self.interpreter.read().get(table_id)

    @property
    def tables(self):
        # Gets a list of tables in this database 
        table_dict = self.interpreter.read()
        return list(map(lambda x: Table(self, x), table_dict))

    def get_table(self, table_name: str) -> Table:
        # get a specific table from table name
        tables = list(filter(lambda x: x.name == table_name, self.tables))
        return tables[0] if tables else None

    def update_table(self, table_id: str, new_dict:dict):
        # update a specific table based on id
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
            r_class = self.__column_types[name]
            r_dict[name] = c_confirm(r_class, value)
            self.table.d_rows = set_key(self.table.d_rows, self.row_id, r_dict)
        else:
            return super().__setattr__(name, value)

    def __getattr__(self, name):
        if self.__rowdict.get(name) != None:
            return c_confirm(self.__column_types[name], self.__rowdict.get(name), raw=False)

    @property
    def dict(self):
        pdict = self.__dict__
        for key in self.__rowdict:
            value = self.__rowdict.get(key)
            clss = self.__column_types.get(key)
            pdict[key] = c_confirm(clss, value, raw=False)
        return pdict

if __name__ == "__main__":
    print("U should close that program huh?")