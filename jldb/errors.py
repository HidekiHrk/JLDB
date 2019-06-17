# This is only for custom exception names lol
class ColumnError(BaseException):
    """
        Column error.
    """
    pass

class TableNotFoundError(BaseException):
    """
        Table not found error
    """
    pass

if __name__ == "__main__":
    print("That's an error file, get out here!!! >:[")