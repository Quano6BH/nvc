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
        SERVER = self.get_server_creds()
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
            + f"WHERE (TIMESTAMPDIFF(day, FromDate, '{today}') ) >= 0 AND CollectionId = {collection_id} "
            + "ORDER BY FromDate DESC LIMIT 1 ;"
        )
        result = self.cursor.fetchall()
        self.sql.close()
        return (result[0][0], result[0][1], result[0][2], result[0][3])

    # def fetch_collection_update(self, data_to_fetch, collection_id):
    #     self.cursor.execute(
    #         f"SELECT {data_to_fetch},Id FROM NVC.CollectionUpdate WHERE CollectionId = {str(collection_id)} ORDER BY Id DESC LIMIT 1"
    #     )
    #     result = self.cursor.fetchone()
    #     self.sql.close()
    #     return result

    # def fetch_holder_by_date(self, collection_id, snapshot_date):
    #     self.cu
