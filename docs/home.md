# Docs: Home

**Classes:**
- [Client](https://github.com/HidekiHrk/JLDB/blob/master/docs/client.md)
- [Table](https://github.com/HidekiHrk/JLDB/blob/master/docs/table.md)
- [Row](https://github.com/HidekiHrk/JLDB/blob/master/docs/row.md)

*I know, it's so much simple xD*

**Getting Started**
```python
from jldb import Client

client = Client(filename="data.jldb")

client.add_table("users", id=int, name=str, age=int, money=float)

users = client.get_table("users")
users.add_row(id=0, name="bar", age=22, money=300.0)
foo = users.get_first(id=0)
print(foo.id, foo.name, foo.age, foo.money)

# output: 0 bar 22 300.0
```
