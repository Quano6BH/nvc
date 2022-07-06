import MySQLdb
import json
from datetime import datetime

def get_server_creds():
    with open("sql_creds.json","r") as f:
        return json.loads(f.read())

SERVER = get_server_creds()
sql = MySQLdb.connect(host=SERVER['host'], port=SERVER['port'], user=SERVER['username'], password=SERVER['password'], database=SERVER['database'])
cursor = sql.cursor()

with open("discord.txt","r") as f:
    accounts = f.readlines()
for account in accounts:
    account = account.replace("\n","")
    email = account.split("|")[0]
    password = account.split("|")[1]
    two_fa = account.split("|")[2]
    token = account.split("|")[3]
    profile_name = account.split("|")[4]
    query = f'''INSERT INTO Discord VALUES ('{email}', '{password}', '{two_fa}', '{token}',  '{profile_name}','{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}', '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}')'''
    print(query)
    cursor.execute(query)

# with open("twitter.txt","r") as f:
#     accounts = f.readlines()
# for account in accounts:
#     account = account.replace("\n","")
#     username = account.split("|")[0]
#     password = account.split("|")[1]
#     two_fa = account.split("|")[2]
#     recovery_email = account.split("|")[3]
#     recovery_password = account.split("|")[4]
#     profile = account.split("|")[5]
#     query = f'''INSERT INTO Twitter VALUES ('{username}', '{password}', '{two_fa}', '{recovery_email}', '{recovery_password}', '{profile}', '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}', '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}')'''
#     print(query)
#     cursor.execute(query)

sql.commit()
cursor.close()