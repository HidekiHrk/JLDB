import jldb

client = jldb.Client('datinha.jldb')
client.add_table('users', id=int, name=str, inventory=dict, coins=float)
users = client.get_table('users')
# users.add_row(id=0, name="hideki", inventory={'a':1}, coins=10)
print(users.rows[1])