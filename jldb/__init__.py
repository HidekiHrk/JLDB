if not __package__:
    exec("import dbclasses as main")
    exec("from errors import *")
else:
    import jldb.dbclasses as main
    from jldb.errors import *

Client = main.Client

if __name__ == "__main__":
    print("Hi! Idk what I'll put in there :(")