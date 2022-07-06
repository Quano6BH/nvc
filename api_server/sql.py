import MySQLdb
import json


class SqlConnector:
    TWITTER_TABLE_NAME = "Twitter"
    DISCORD_TABLE_NAME = "Discord"

    def __init__(self):
        SERVER = self.get_server_creds()
        self.sql = MySQLdb.connect(host=SERVER['host'], port=SERVER['port'],
                                   user=SERVER['username'], password=SERVER['password'], database=SERVER['database'])
        self.cursor = self.sql.cursor()

    def get_server_creds(self):
        with open("sql_creds.json", "r") as f:
            return json.loads(f.read())

    def fetch_table(self, table_name):
        self.cursor.execute(f"SELECT * from {table_name};")
        result = self.cursor.fetchall()
        self.sql.close()
        return result

    def insert_row(self, table_name, data):
        columns = ', '.join(data.keys())

        values = ', '.join([f"'{item}'" if isinstance(
            item, str) else item for item in data.values()])

        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values});"

        print(query)

        self.cursor.execute(query)
        self.sql.commit()
        self.sql.close()

    def update_row(self, table_name, data, condition):

        values = ', '.join([f"{key}='{data[key]}'" if isinstance(
            data[key], str) else f"{key}={data[key]}" for key in data.keys()])

        query = f"UPDATE {table_name} SET {values} WHERE {condition}"

        print(query)

        self.cursor.execute(query)
        self.sql.commit()
        self.sql.close()

    def delete_row(self, table_name, data):
        query = f"DELETE FROM {table_name} WHERE {data}"
        print(query)
        self.cursor.execute(query)
        self.sql.commit()
        self.sql.close()

    def upsert_row(self, table_name, datas):

        columns = ', '.join(datas[0].keys())
        values = []
        for data in datas:

            value = ', '.join([f"'{item}'" if isinstance(
                item, str) else item for item in data.values()])
            values.append(f"({value})")
        value_str = ",".join(values)
        query = f"REPLACE INTO {table_name} ({columns}) VALUES {value_str}"

        print(query)

        self.cursor.execute(query)
        self.sql.commit()
        self.sql.close()
