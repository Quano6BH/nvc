from datetime import datetime
import MySQLdb
import json


class SqlConnector:
    WALLET_TABLE_NAME = "NVC.Wallet"
    COLLECTION_TABLE_NAME = "NVC.Collection"
    COLLECTION_UPDATE_TABLE_NAME = "NVC.CollectionUpdate"
    NFT_TABLE_NAME = "NVC.Nft"
    NFT_HOLDER_TABLE_NAME = "NVC.NftHolder"
    NFT_HOLDER_BY_DATE_TABLE_NAME = "NVC.HolderByDate"
    NFT_HOLDER_BY_MONTH_TABLE_NAME = "NVC.HolderByMonth"

    def __init__(self):
        SERVER = {
            "host": "34.87.174.70",
            "port": 3306,
            "username": "root",
            "password": "Nvc123!@#",
            "database": "NVC",
        }
        self.sql = MySQLdb.connect(host=SERVER['host'], port=SERVER['port'],
                                   user=SERVER['username'], password=SERVER['password'], database=SERVER['database'])
        self.cursor = self.sql.cursor()

    def get_collection_by_id(self, collection_id):  # Get Collection
        query = f"SELECT Id, StartDate, EndDate, Ipfs, TotalSuppply, Address, NetworkId FROM {self.COLLECTION_TABLE_NAME} "\
                + f"WHERE Id = {str(collection_id)};"

        self.cursor.execute(query)

        result = self.cursor.fetchone()

        self.sql.close()

        if not result:
            return None

        id, start_date, end_date, ipfs, total_supply, address, network_id = result
        return {
            "id": id,
            "start_date": start_date,
            "end_date": end_date,
            "ipfs": ipfs,
            "total_supply": total_supply,
            "address": address,
            "network_id": network_id
        }

    def get_nft(self, collection_id, token_id, wallet_address, snapshot_date=None):  # Detail NFT
        snapshot_date = snapshot_date or datetime.date.now()

        query = f"SELECT Id, Holder, TokenId, CollectionId, HoldDays, HoldDaysInMonth, InterestEarned, InterestEarnedInMonth, SnapshotDate "\
            + f"FROM {self.NFT_HOLDER_BY_DATE_TABLE_NAME} "\
            + f"WHERE CollectionId = {str(collection_id)} "\
            + f"AND TokenId = {str(token_id)} "\
            + f"AND Holder = {wallet_address} "\
            + f"AND SnapshotDate = {str(snapshot_date)};"

        self.cursor.execute(query)

        result = self.cursor.fetchone()

        self.sql.close()

        if not result:
            return None

        id, holder, query_token_id, query_collection_id, hold_days, hold_days_in_month, interest_earned, interest_earned_in_month, query_snapshot_date = result
        return {
            "id": id,
            "holder": holder,
            "token_id": query_token_id,
            "collection_id": query_collection_id,
            "hold_days": hold_days,
            "hold_days_in_month": hold_days_in_month,
            "interest_earned": interest_earned,
            "interest_earned_in_month": interest_earned_in_month,
            "snapshot_date": query_snapshot_date
        }
# {
# 	currentOwner:"0x..",
# 	holdDaysInCurrentMonth: 3,//number of days the NFT owned by the owner
# 	collectionId: 1,
# 	earnings:[
# 		{
# 			month:1,//1-12,
# 			principalEarned:12,//by $,gốc nhận được của tháng 1
# 			interestEarned:0.1//by $, lãi nhận được của tháng 1
# 			interestRate:0.1//by %, % lãi của tháng
# 			principalRate:20//by $, tiền gốc mỗi NFT của tháng
# 		}
# 	]
# }

    def get_collection_stats(self, collection_id, snapshot_date=None):  # Collection Report
        snapshot_date = snapshot_date or datetime.date.now()

        query = f"SELECT Id, Holder, TokenId, CollectionId, HoldDays, HoldDaysInMonth, InterestEarned, InterestEarnedInMonth, SnapshotDate "\
                + f"FROM {self.NFT_HOLDER_BY_DATE_TABLE_NAME} "\
                + f"WHERE CollectionId = {str(collection_id)} "\
                + f"AND SnapshotDate = {str(snapshot_date)};"

        self.cursor.execute(query)

        result = self.cursor.fetchall()

        self.sql.close()
        if not result:
            return None

        data = []
        for row in result:
            id, holder, query_token_id, query_collection_id, hold_days, hold_days_in_month, interest_earned, interest_earned_in_month, query_snapshot_date = row
            data.append({
                "id": id,
                "holder": holder,
                "token_id": query_token_id,
                "collection_id": query_collection_id,
                "hold_days": hold_days,
                "hold_days_in_month": hold_days_in_month,
                "interest_earned": interest_earned,
                "interest_earned_in_month": interest_earned_in_month,
                "snapshot_date": query_snapshot_date
            })

        return data

    def get_wallet_nfts(self, collection_id, wallet_address, snapshot_date=None):
        snapshot_date = snapshot_date or datetime.date.now()

        query = f"SELECT TokenId, Ho FROM {self.NFT_HOLDER_BY_DATE_TABLE_NAME} "\
                + f"WHERE CollectionId = {str(collection_id)} "\
                + f"AND Holder = {wallet_address} "\
                + f"AND SnapshotDate = {str(snapshot_date)};"

        self.cursor.execute(query)

        result = self.cursor.fetchall()

        self.sql.close()
        if not result:
            return None

        data = []
        for row in result:
            id, holder, query_token_id, query_collection_id, hold_days, hold_days_in_month, interest_earned, interest_earned_in_month, query_snapshot_date = row
            data.append({
                "id": id,
                "holder": holder,
                "token_id": query_token_id,
                "collection_id": query_collection_id,
                "hold_days": hold_days,
                "hold_days_in_month": hold_days_in_month,
                "interest_earned": interest_earned,
                "interest_earned_in_month": interest_earned_in_month,
                "snapshot_date": query_snapshot_date
            })

        return data

    def fetch_closest_update(self, today, collection_id):
        self.cursor.execute(
            "SELECT FromDate,Principal,Interest,Id FROM NVC.CollectionUpdate "
            + f"WHERE (TIMESTAMPDIFF(day, FromDate, '{today}') ) >= 0 AND CollectionId = {str(collection_id)} "
            + "ORDER BY FromDate DESC LIMIT 1 ;"
        )
        result = self.cursor.fetchall()
        self.sql.close()
        return (result[0][0], result[0][1], result[0][2], result[0][3])


sql = SqlConnector()
print(sql.get_collection_by_id(1))
print(sql.get_wallet_nfts(1, "0x", datetime.date.now()))
print(sql.get_nft(1, 1, datetime.date.now()))
print(sql.get_wallet_nfts(1, "0x", datetime.date.now()))
