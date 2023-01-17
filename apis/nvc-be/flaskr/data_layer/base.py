from MySQLdb import connect
from MySQLdb.connections import Connection
from MySQLdb.cursors import Cursor, DictCursor
from string import Template


class BaseDataLayer:
    WALLET_TABLE_NAME = "Wallet"
    COLLECTION_TABLE_NAME = "Collection"
    COLLECTION_UPDATE_TABLE_NAME = "CollectionUpdate"
    NFT_TABLE_NAME = "Nft"
    NFT_HOLDER_TABLE_NAME = "NftHolder"
    NFT_HOLDER_BY_DATE_TABLE_NAME = "HolderByDate"
    NFT_HOLDER_BY_MONTH_TABLE_NAME = "HolderByMonth"
    CONTRACT_TABLE_NAME = "Contract"

    def __init__(self, db_config):
        self.db_config = db_config

    def create_db_connection(self, db_config) -> Connection:
        return connect(
            host=db_config["host"],
            port=db_config["port"],
            user=db_config["username"],
            password=db_config["password"],
            database=db_config["database"],
        )

    def create_cursor(self, db_conn: Connection) -> Cursor:
        return db_conn.cursor(DictCursor)

    def _on_query_string_generated(self, query):
        print(query)

    def _execute_query(self, cursor: Cursor, query_template, **kwargs):
        query = (Template(query_template).substitute(kwargs))

        self._on_query_string_generated(query)
        cursor.execute(query, kwargs)
        print("Parsed: " + str(cursor._executed))
