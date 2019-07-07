import re
import os

class Interpreter:
    """
        This is an interpreter for the database
    """
    @staticmethod
    def get_dict(txt):
        """
            gets a dict based on db string
        """
        # get table separator #
        txt = txt.split(';')
        # get all tables #
        dicts = list(map(lambda x:re.findall(r'table_[0-9]+=\{.*\}=endtable', x), txt))
        dicts = list(map(lambda z: z[0], filter(lambda x: x, dicts)))
        # get table dicts
        tables = dict(map(lambda x: 
            [re.findall(r'table_[0-9]+', x)[0],
            eval(re.findall(r'\{.*\}', x)[0])],
            dicts))
        return tables

    @staticmethod
    def get_text(dct):
        """
            gets a string based on db dict
        """
        return ';'.join([f"{table_id}={dct[table_id]}=endtable" for table_id in dct])

    def __init__(self, filename="data.jldb", encoding='utf-8'):
        if not os.path.isfile(filename):
            with open(filename, 'w', encoding=encoding) as f:
                pass
        self.filename = filename
        self.encoding = encoding

    def read(self):
        with open(self.filename, 'r', encoding=self.encoding) as dbfile:
            return Interpreter.get_dict(dbfile.read())
    
    def update(self, new_dict):
        with open(self.filename, 'w', encoding=self.encoding) as dbfile:
            dbfile.write(Interpreter.get_text(new_dict))

if __name__ == "__main__":
    print("It seems like you're a B-BAKAAAAAAAA >///<")