import datetime
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
        self.sql = MySQLdb.connect(
            host=SERVER["host"],
            port=SERVER["port"],
            user=SERVER["username"],
            password=SERVER["password"],
            database=SERVER["database"],
        )
        self.cursor = self.sql.cursor()

    def get_collection_by_id(self, collection_id):  # Get Collection
        query = (
            f"SELECT c.Id, StartDate, EndDate, Ipfs, TotalSupply, Address, NetworkId, Principal, Interest, FromDate, Type, Message "
            + f"FROM {self.COLLECTION_TABLE_NAME} c "
            + f"INNER JOIN {self.COLLECTION_UPDATE_TABLE_NAME} cu ON  c.Id = cu.CollectionId "
            + f"WHERE c.Id = {str(collection_id)};"
        )

        self.cursor.execute(query)

        result = self.cursor.fetchall()

        self.sql.close()

        if not result:
            return None
        # for row in result:
        #     id, start_date, end_date, ipfs, total_supply, address, network_id, principal, interest, from_date, type, message = row
        #     data.append({
        #         "id": id,
        #         "start_date": start_date,
        #         "end_date": end_date,
        #         "ipfs": ipfs,
        #         "total_supply": total_supply,
        #         "address": address,
        #         "network_id": network_id,
        #         "principal": principal,
        #         "interest": interest,
        #         "from_date": from_date,
        #         "type": type,
        #         "message": message
        #     })
        (
            id,
            start_date,
            end_date,
            ipfs,
            total_supply,
            address,
            network_id,
            _,
            _,
            _,
            _,
            _,
        ) = result[0]
        return {
            "id": id,
            "startDate": str(start_date),
            "endDate": str(end_date),
            "ipfs": ipfs,
            "totalSupply": total_supply,
            "address": address,
            "networkId": network_id,
            "updates": [
                {
                    "principal": principal,
                    "interest": interest,
                    "from_date": str(from_date),
                    "type": type,
                    "message": message,
                }
                for _, _, _, _, _, _, _, principal, interest, from_date, type, message in result
            ],
        }

    def get_nft_detail_prev_month(
        self, collection_id, token_id, wallet_address, snapshot_date=None
    ):  # Detail NFT
        snapshot_date = snapshot_date or datetime.date.today()

        query = (
            f"SELECT hbm.Holder, hbm.CollectionId, ResetDate, TotalNFTs, hbm.InterestEarned as InterestEarned_hbm, TokenId, HoldDays, HoldDaysInMonth, hbd.InterestEarned as InterestEarned_hbd, InterestEarnedInMonth, SnapshotDate "
            + f"FROM {self.NFT_HOLDER_BY_MONTH_TABLE_NAME} hbm "
            + f"INNER JOIN {self.NFT_HOLDER_BY_DATE_TABLE_NAME} hbd "
            + f"ON hbm.CollectionId = hbd.CollectionId AND hbm.Holder = hbd.Holder AND hbm.ResetDate = hbd.SnapshotDate "
            + f"WHERE hbm.CollectionId = {str(collection_id)} "
            + f"AND hbm.Holder = '{wallet_address}' "
            + f"AND hbd.TokenId = '{str(token_id)}' "
            + f"AND ResetDate <= '{str(snapshot_date)}';"
        )
        print(query)
        self.cursor.execute(query)

        result = self.cursor.fetchall()

        self.sql.close()

        if not result:
            return None

        (
            hbm_holder,
            hbm_collection_id,
            hbm_reset_date,
            hbm_total_nfts,
            hbm_interest_earned,
            row_token_id,
            _,
            _,
            _,
            _,
            _,
        ) = result[0]
        data = {
            "currentOwner": hbm_holder,
            "holdDaysInCurrentMonth": 0,
            "tokenId": row_token_id,
            "collectionId": hbm_collection_id,
            "earnings": [],
        }
        for row in result:
            (
                hbm_holder,
                hbm_collection_id,
                hbm_reset_date,
                hbm_total_nfts,
                hbm_interest_earned,
                _,
                _,
                _,
                _,
                _,
                _,
            ) = row
            (
                _,
                _,
                _,
                _,
                _,
                row_token_id,
                hold_days,
                hold_days_in_month,
                hbd_interest_earned,
                hbd_interest_earned_in_month,
                row_snapshot_date,
            ) = row
            data["earnings"].append(
                {
                    "datetime": str(row_snapshot_date),
                    "collection_id": hbm_collection_id,
                    "interestEarned": hbd_interest_earned,
                }
            )

        return data

    # Detail NFT
    def get_nft_detail_current_month(
        self, collection_id, token_id, wallet_address, snapshot_date=None
    ):
        snapshot_date = snapshot_date or datetime.date.today()

        query = (
            f"SELECT Id, Holder, TokenId, CollectionId, HoldDays, HoldDaysInMonth, InterestEarned, InterestEarnedInMonth, SnapshotDate "
            + f"FROM {self.NFT_HOLDER_BY_DATE_TABLE_NAME} "
            + f"WHERE CollectionId = {str(collection_id)} "
            + f"AND TokenId = {str(token_id)} "
            + f"AND Holder = '{wallet_address}' "
            + f"AND SnapshotDate = '{str(snapshot_date)}';"
        )

        self.cursor.execute(query)

        result = self.cursor.fetchone()

        self.sql.close()

        if not result:
            return None

        (
            id,
            holder,
            query_token_id,
            query_collection_id,
            hold_days,
            hold_days_in_month,
            interest_earned,
            interest_earned_in_month,
            query_snapshot_date,
        ) = result
        return {
            "id": id,
            "holder": holder,
            "token_id": query_token_id,
            "collection_id": query_collection_id,
            "hold_days": hold_days,
            "hold_days_in_month": hold_days_in_month,
            "interest_earned": interest_earned,
            "interest_earned_in_month": interest_earned_in_month,
            "snapshot_date": query_snapshot_date,
        }

    def get_collection_stats(
        self, collection_id, snapshot_date=None
    ):  # Collection Report
        snapshot_date = snapshot_date or datetime.date.today()

        query = (
            f"SELECT Id, Holder, TokenId, CollectionId, HoldDays, HoldDaysInMonth, InterestEarned, InterestEarnedInMonth, SnapshotDate "
            + f"FROM {self.NFT_HOLDER_BY_DATE_TABLE_NAME} "
            + f"WHERE CollectionId = {str(collection_id)} "
            + f"AND SnapshotDate = {str(snapshot_date)};"
        )

        self.cursor.execute(query)

        result = self.cursor.fetchall()

        self.sql.close()
        if not result:
            return None

        data = []
        for row in result:
            (
                id,
                holder,
                query_token_id,
                query_collection_id,
                hold_days,
                hold_days_in_month,
                interest_earned,
                interest_earned_in_month,
                query_snapshot_date,
            ) = row
            data.append(
                {
                    "id": id,
                    "holder": holder,
                    "token_id": query_token_id,
                    "collection_id": query_collection_id,
                    "hold_days": hold_days,
                    "hold_days_in_month": hold_days_in_month,
                    "interest_earned": interest_earned,
                    "interest_earned_in_month": interest_earned_in_month,
                    "snapshot_date": query_snapshot_date,
                }
            )

        return data

    def get_wallet_nfts(self, collection_id, wallet_address, snapshot_date=None):
        snapshot_date = snapshot_date or datetime.date.today()

        query = (
            f"SELECT TokenId, Ho FROM {self.NFT_HOLDER_BY_DATE_TABLE_NAME} "
            + f"WHERE CollectionId = {str(collection_id)} "
            + f"AND Holder = {wallet_address} "
            + f"AND SnapshotDate = {str(snapshot_date)};"
        )

        self.cursor.execute(query)

        result = self.cursor.fetchall()

        self.sql.close()
        if not result:
            return None

        data = []
        for row in result:
            (
                id,
                holder,
                query_token_id,
                query_collection_id,
                hold_days,
                hold_days_in_month,
                interest_earned,
                interest_earned_in_month,
                query_snapshot_date,
            ) = row
            data.append(
                {
                    "id": id,
                    "holder": holder,
                    "token_id": query_token_id,
                    "collection_id": query_collection_id,
                    "hold_days": hold_days,
                    "hold_days_in_month": hold_days_in_month,
                    "interest_earned": interest_earned,
                    "interest_earned_in_month": interest_earned_in_month,
                    "snapshot_date": query_snapshot_date,
                }
            )

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

    def get_unique_holder(self, collection_id, snapshot_date=None):
        snapshot_date = snapshot_date or datetime.date.today()
        self.cursor.execute(
            "SELECT count(distinct Holder) FROM NVC.HolderByDate "
            + f"WHERE SnapshotDate = '{snapshot_date}' AND Holding = 1 AND CollectionId = {collection_id};"
        )
        result = self.cursor.fetchone()
        self.sql.close()
        return result[0]

    def get_total_pay(self, collection_id, snapshot_date=None):
        snapshot_date = snapshot_date or datetime.date.today()
        self.cursor.execute(
            "SELECT sum(InterestEarned) FROM NVC.HolderByDate "
            + f"WHERE SnapshotDate = '{snapshot_date}' AND CollectionId = {collection_id};"
        )
        result = self.cursor.fetchone()
        self.sql.close()
        return result[0]

    def get_report_data(self, collection_id, snapshot_date=None):
        snapshot_date = snapshot_date or datetime.date.today()
        self.cursor.execute(
            "SELECT Principal, Interest, TotalSupply "
            + "FROM NVC.CollectionUpdate cu "
            + "INNER JOIN NVC.Collection c ON cu.CollectionId = c.Id "
            + f"WHERE (TIMESTAMPDIFF(day, FromDate, '{snapshot_date}') ) >= 0 AND CollectionId = {collection_id} AND Type = 'Update' "
            + "ORDER BY FromDate DESC LIMIT 1 ;"
        )
        result = self.cursor.fetchall()
        self.sql.close()
        return (result[0][0], result[0][1], result[0][2])


# collection_id = 1
# nft_id = 8
# wallet_address = "0xd9A98d4b857C8a8c8D76Fd8E8904a0a29B915138"
# sql = SqlConnector()
# nft_prev_months = sql.get_nft_detail_prev_month(collection_id, nft_id, wallet_address)

# print(nft_prev_months)
# sql = SqlConnector()
# nft_current = sql.get_nft_detail_prev_month(
#     collection_id, nft_id, wallet_address)
# nft_prev_months["holdDaysInCurrentMonth"] = nft_current["hold_days_in_month"]
# nft_prev_months["earnings"].append({
#     "datetime": nft_current["snapshot_date"],
#     "collectionId": nft_current["collection_id"],
#     "interestEarned": nft_current["interest_earned_in_month"],
# })
# print(nft_prev_months)
