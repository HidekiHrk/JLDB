from jldb.main import *

client = Client()

print(client.tables)
client.add_table("admins", id = int, name = str, money = float)
print(client.get_table('admins').rows)