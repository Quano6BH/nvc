import MySQLdb
import json


class SqlConnector:
    WALLET_TABLE_NAME = "Wallet"
    COLLECTION_TABLE_NAME = "Collection"
    COLLECTION_UPDATE_TABLE_NAME = "CollectionUpdate"
    NFT_TABLE_NAME = "Nft"
    NFT_HOLDER_TABLE_NAME = "NftHolder"
    NFT_HOLDER_BY_DATE_TABLE_NAME = "HolderByDate"
    NFT_HOLDER_BY_MONTH_TABLE_NAME = "HolderByMonth"

    def __init__(self):
        SERVER = {
            "host":"34.87.147.70",
            "port":3306,
            "username":"root",
            "password":"NVC123!@#",
            "database":"NVC",
        }
        self.sql = MySQLdb.connect(host=SERVER['host'], port=SERVER['port'],
                                   user=SERVER['username'], password=SERVER['password'], database=SERVER['database'])
        self.cursor = self.sql.cursor()

    def get_collection_by_id(self, collection_id):  # Get Collection
        pass

    def get_nft(self, collection_id, nft_id, wallet):  # Detail NFT
        pass

    def get_collection_stats(self, collection_id):  # Collection Report
        pass

    def get_wallet(self, wallet_address):  # Get Wallet
        pass
