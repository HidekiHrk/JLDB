# Docs: Client

**Methods:**

**➡** add_table(table_name, **columns) : *adds a table to the database. Example:*
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
