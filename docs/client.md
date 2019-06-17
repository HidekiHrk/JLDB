# Docs: Client

### Properties:

**➡** interpreter : *the db file interpreter, don't touch it if you don't know what you're doing*

**➡** tables : *a list of tables in the database*

### Methods:

**➡** add_table(table_name: str, **columns) : *adds a table to the database. Example:*
```python
client.add_table("foo", bar=str, money=float)
```
*User-defined classes are welcome into the table definition. Example:*
```python
class Foo:
  def__init__(self, name):
    self.name = name

bar_table = client.add_table("bar", foo=Foo, number=int)
bar_table.add_row(foo=Foo("bar"), number=1)
row1 = bar_table.get_first(number=1)
print(row1.foo.name)

# output: bar
```
*Return: [Table](https://github.com/HidekiHrk/JLDB/blob/master/docs/table.md)*

**➡** remove_table(table_id: str) : *it's like "add_table", but it removes a table from the database.*

**➡** get_table(table_name: str) : *gets a table by the name.*
