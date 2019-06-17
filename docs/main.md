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

client.create_table("users", id=int, name=str, age=int, money=float)

users = client.get_table("users")
users.add_row(id=0, name="Foo", age=22, money=300.0)
print(users.get_first(id=0).name)
```
