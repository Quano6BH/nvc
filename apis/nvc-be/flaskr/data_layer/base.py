import MySQLdb
from string import Template


class BaseDataLayer:
    WALLET_TABLE_NAME = "NVC.Wallet"
    COLLECTION_TABLE_NAME = "NVC.Collection"
    COLLECTION_UPDATE_TABLE_NAME = "NVC.CollectionUpdate"
    NFT_TABLE_NAME = "NVC.Nft"
    NFT_HOLDER_TABLE_NAME = "NVC.NftHolder"
    NFT_HOLDER_BY_DATE_TABLE_NAME = "NVC.HolderByDate"
    NFT_HOLDER_BY_MONTH_TABLE_NAME = "NVC.HolderByMonth"

    def __init__(self, db_config):
        self.db_config = db_config

    def create_db_connection(self, db_config):
        return MySQLdb.connect(
            host=db_config["host"],
            port=db_config["port"],
            user=db_config["username"],
            password=db_config["password"],
            database=db_config["database"],
        )

    def _on_query_string_generated(self, query):
        print(query)

    def _execute_query(self, cursor, query_template, **kwargs):
        query = (Template(query_template).substitute(kwargs))

        self._on_query_string_generated(query)

        cursor.execute(query)