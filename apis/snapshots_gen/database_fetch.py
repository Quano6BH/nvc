import MySQLdb
import json


class SqlConnector:
    COLLECTION = "NVC.Collection"
    COLLECTIONUPDATE = "NVC.CollectionUpdate"
    HOLDERBYDATE = "NVC.HolderByDate"
    HOLDERBYMONTH = "NVC.HolderByMonth"
    NFT = "NVC.Nft"
    NFTHOLDER = "NftHolder"
    WALLET = "NVC.Wallet"

    def __init__(self):
        SERVER = {
            "host": "34.87.174.70",
            "port": 3306,
            "username": "root",
            "password": "Nvc123!@#",
            "database": "NVC",
        }
        self.sql = MySQLdb.connect(
            host=SERVER["host"],
            port=SERVER["port"],
            user=SERVER["username"],
            password=SERVER["password"],
            database=SERVER["database"],
        )
        self.cursor = self.sql.cursor()

    def get_server_creds(self):
        with open("sql_creds.json", "r") as f:
            return json.loads(f.read())

    def execute_script(self, script):
        self.cursor.execute(script)
        self.sql.commit()
        self.sql.close()

    def fetch_table(self, table_name):
        self.cursor.execute(f"SELECT * FROM {table_name};")
        result = self.cursor.fetchall()
        self.sql.close()
        return result

    def insert_row(self, table_name, data):
        columns = ", ".join(data.keys())

        values = ", ".join(
            [f"'{item}'" if isinstance(item, str) else item for item in data.values()]
        )

        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values});"

        print(query)

        self.cursor.execute(query)
        self.sql.commit()
        self.sql.close()

    def update_row(self, table_name, data, condition):

        values = ", ".join(
            [
                f"{key}='{data[key]}'"
                if isinstance(data[key], str)
                else f"{key}={data[key]}"
                for key in data.keys()
            ]
        )

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

        columns = ", ".join(datas[0].keys())
        values = []
        for data in datas:

            value = ", ".join(
                [
                    f"'{item}'" if isinstance(item, str) else item
                    for item in data.values()
                ]
            )
            values.append(f"({value})")
        value_str = ",".join(values)
        query = f"REPLACE INTO {table_name} ({columns}) VALUES {value_str}"

        print(query)

        self.cursor.execute(query)
        self.sql.commit()
        self.sql.close()

    def fetch_wallet(self, wallet):
        self.cursor.execute(
            f"SELECT * FROM {self.HOLDERBYDATE} WHERE Holder = {wallet};"
        )
        result = self.cursor.fetchall()
        self.sql.close()
        return result

    def fetch_closest_update(self, today, collection_id):
        self.cursor.execute(
            "SELECT FromDate,Principal,Interest,Id FROM NVC.CollectionUpdate "
            + f"WHERE (TIMESTAMPDIFF(day, FromDate, '{today}') ) < 0 AND CollectionId = {collection_id} AND Type = 'Update'"
            + "ORDER BY FromDate ASC LIMIT 1 ;"
        )
        result = self.cursor.fetchall()
        self.sql.close()
        return (result[0][0], result[0][1], result[0][2], result[0][3])

    def fetch_report(self, snapshot_date, collection_id):
        self.cursor.execute(
            f"SELECT Holder, TokenId, HoldDays, HoldDaysInMonth, InterestEarned, InterestEarnedInMonth, SnapshotDate FROM NVC.HolderByDate WHERE SnapshotDate = '{snapshot_date}' AND CollectionId = {collection_id};"
        )
        result = self.cursor.fetchall()
        self.sql.close()
        data = {}
        for row in result:
            interest = float(row[4])
            interest_in_month = float(row[5])
            try:
                data[row[0]]["token_ids"][f"{row[1]}"] = {
                    "holding_day": row[2],
                    "holding_day_in_month": row[3],
                    "interest": interest,
                    "interest_in_month": interest_in_month,
                }
            except:
                data[row[0]] = {
                    "token_ids": {
                        f"{row[1]}": {
                            "holding_day": row[2],
                            "holding_day_in_month": row[3],
                            "interest": interest,
                            "interest_in_month": interest_in_month,
                        }
                    }
                }
                continue
        return data
