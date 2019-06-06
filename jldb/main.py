import re
from jldb.interpreter import Interpreter

class Client(object):
    def __init__(self, filename="data.jldb"):
        self.interpreter = Interpreter(filename=filename)
    
    def add_table(self, table_name: str, **columns):
        tables = self.interpreter.read()
        tables_last_id = list(tables)[-1] if len(tables) else None
        new_id = int(tables_last_id[len("table_"):]) + 1 if tables_last_id else 0
        table_dict = 