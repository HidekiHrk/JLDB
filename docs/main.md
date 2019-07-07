# Docs

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
client.commit()

# output: 0 bar 22 300.0
```

*All db classes have support to with statements*

**Example**
```python
from jldb import Client

with Client(filename="data.jldb") as client:
    client.add_table("users", id=int, name=str, age=int, money=float)
    
    with client.get_table("users") as users:
        users.add_row(id=0, name="bar", age=22, money=300.0)
        
        with users.get_first(id=0) as foo:
            print(foo.id, foo.name, foo.age, foo.money)

# output: 0 bar 22 300.0
```
*Obs: each with statement will finish with a commit to the table. So, it's not smart to use nested with statements as used above;*