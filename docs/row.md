# Docs: Row

##### [Return to the docs](https://github.com/HidekiHrk/JLDB/blob/master/docs/main.md)

### Properties:

**->** table : *the [Table](https://github.com/HidekiHrk/JLDB/blob/master/docs/table.md) object wich the row is stored;*

**->** row_id : *the row id. each row have a unique id in the table; type: int;*

**->** dict : *a dict with all row properties (including the data stored on row);*

*Each row can modify freely its data by accessing them like properties. Example:*
```python
row1 = table1.get_first(name="foo")
print(row1.name) # foo
row1.name = "bar"
print(table1.get_first(name="foo")) # None
print(table1.get_first(name="bar")) # <jldb.__main__.Row object at 0x00000000000>
```

### Methods:

**->** save() : *commits the row to the table;*

**->** delete() : *deletes the row from the table;*
