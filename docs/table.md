# Docs: Table

##### [Return to the docs](https://github.com/HidekiHrk/JLDB/blob/master/docs/main.md)

### Properties:

**➡** client : *[Client](https://github.com/HidekiHrk/JLDB/blob/master/docs/client.md) object of the database wich this table is stored in;*

**➡** id : *this is the table id, each table have an unique id that's used to identificate each one on the [Client](https://github.com/HidekiHrk/JLDB/blob/master/docs/client.md) obj;*

**➡** name : *this is the table name;*

**➡** columns : *returns a list of columns in this table;*

**➡** rows : *return a list of [Row](https://github.com/HidekiHrk/JLDB/blob/master/docs/row.md) objects stored on this table;*

### Methods:

**➡** get_rows(**cols) : *returns a list of [Row](https://github.com/HidekiHrk/JLDB/blob/master/docs/row.md) objects that matches with the value of parameters passed on the function. Example:*

```python
rows = table.get_rows(name="foo")
for row in rows:
  print(row.name)

""" output:
  foo
  foo
  foo
  ...
"""
```

**➡** get_first(**cols) : *it's like "get_rows", but this one returns the first [Row](https://github.com/HidekiHrk/JLDB/blob/master/docs/row.md) object that matches with the parameters passed;*

**➡** add_row(**cols) : *adds a row to the table based on parameters passed on the function. Example:*
```python
table.add_row(name="foo", id=1)
```
*Return: [Row](https://github.com/HidekiHrk/JLDB/blob/master/docs/row.md)*

**➡** remove_row(row_id: int) : *removes a row based on id;*

**➡** add_column(cname: str, ctype) : *add a column to the table with a given name and type;*

**➡** remove_column(cname: str) : *remove a column based on name;*

**➡** delete() : *deletes the entire current table from the database; (make sure that you won't use any references of this table, otherwise it will result in a TableNotFoundError);*
