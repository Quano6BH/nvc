import datetime
import MySQLdb
from string import Template


class SqlConnector:
    WALLET_TABLE_NAME = "NVC.Wallet"
    COLLECTION_TABLE_NAME = "NVC.Collection"
    COLLECTION_UPDATE_TABLE_NAME = "NVC.CollectionUpdate"
    NFT_TABLE_NAME = "NVC.Nft"
    NFT_HOLDER_TABLE_NAME = "NVC.NftHolder"
    NFT_HOLDER_BY_DATE_TABLE_NAME = "NVC.HolderByDate"
    NFT_HOLDER_BY_MONTH_TABLE_NAME = "NVC.HolderByMonth"

    def __init__(self, config):
        SERVER = {
            "host": "34.87.174.70",
            "port": 3306,
            "username": "root",
            "password": "Nvc123!@#",
            "database": "NVC",
        }
        self.connection = MySQLdb.connect(
            host=SERVER["host"],
            port=SERVER["port"],
            user=SERVER["username"],
            password=SERVER["password"],
            database=SERVER["database"],
        )

    def _on_query_string_generated(self, query):
        print(query)

    def _execute_query(self, cursor, query_template, **kwargs):
        query = (Template(query_template).substitute(kwargs))

        self._on_query_string_generated(query)

        cursor.execute(query)

    def get_collection_with_updates_by_id(self, collection_id, asd):
        data = self.get_collection_with_updates_by_id(collection_id)
        if not data:
            return None
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
            buy_back_o,
            _,
        ) = data[0]

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
                    "buyBack": str(buy_back)[-2] == "1",
                    "id": cu_id,
                }
                for _, _, _, _, _, _, _, principal, interest, from_date, type, message, buy_back, cu_id in result
            ],
        }

    get_collection_with_updates_by_id_query_template = f'''
        SELECT c.Id, StartDate, EndDate, Ipfs, TotalSupply,Address,  " +
        NetworkId, Principal, Interest, FromDate, Type, Message, BuyBack, cu.Id " +
        FROM {COLLECTION_TABLE_NAME} c " +
        INNER JOIN {COLLECTION_UPDATE_TABLE_NAME} cu "
        ON  c.Id = cu.CollectionId " +
        WHERE c.Id = $collection_id;"
    '''

    def get_collection_with_updates_by_id(self, collection_id):

        with self.connection.cursor() as cursor:
            self._execute_query(
                cursor=cursor,
                query_template=self.get_collection_with_updates_by_id_query_template,
                collection_id=collection_id
            )

            return cursor.fetchall()

    def get_nft_history(
        self, collection_id, token_id, wallet_address
    ):
        result = self.get_nft_history(collection_id, token_id, wallet_address)
        if not result:
            return None
        earnings = []

        for row in result:
            _, _, _, row_snapshot_date, interest, principal, paid, updateAppliedId = row
            earnings.append(
                {
                    "datetime": str(row_snapshot_date),
                    "paid": paid == b"\x01",
                    "interestRate": interest,
                    "principal": principal,
                    "updateAppliedId": updateAppliedId,
                }
            )

        return earnings

    get_nft_history_query_template = f'''
        SELECT hbm.Holder, hbm.CollectionId, hbd.TokenId, SnapshotDate, 
                cu.Interest, cu.Principal, hbm.Paid, hbm.UpdateAppliedId 
        FROM {NFT_HOLDER_BY_MONTH_TABLE_NAME} hbm 
            INNER JOIN {NFT_HOLDER_BY_DATE_TABLE_NAME} hbd 
            ON hbm.CollectionId = hbd.CollectionId 
            AND hbm.Holder = hbd.Holder 
            AND hbm.ResetDate = hbd.SnapshotDate 
            INNER JOIN {COLLECTION_UPDATE_TABLE_NAME} cu 
            ON cu.Id = hbm.UpdateAppliedId  
        WHERE hbm.CollectionId = $collection_id
        AND hbm.Holder = '$wallet_address' 
        AND hbd.TokenId = '$token_id';
    '''

    def get_nft_history(
        self, collection_id, token_id, wallet_address
    ):

        with self.connection.cursor() as cursor:

            self._execute_query(
                cursor=cursor,
                query_template=self.get_nft_history_query_template,
                collection_id=collection_id,
                token_id=token_id,
                wallet_address=wallet_address
            )

            return cursor.fetchall()

    get_nft_current_query_template = f'''
        SELECT hbd.Holder, hbd.CollectionId, hbd.TokenId, SnapshotDate, 
                     cu.Interest, cu.Principal, hbd.UpdateAppliedId, hbd.HoldDaysinMonth 
        FROM {NFT_HOLDER_BY_DATE_TABLE_NAME} hbd 
            INNER JOIN {COLLECTION_UPDATE_TABLE_NAME} cu 
            ON cu.Id = hbd.UpdateAppliedId  
        WHERE hbd.CollectionId = $collection_id
        AND hbd.Holder = '$wallet_address' 
        AND hbd.SnapshotDate = '$snapshot_date' 
        AND hbd.TokenId = '$token_id';
    '''

    def get_nft_current(
        self, collection_id, token_id, wallet_address, snapshot_date=None
    ):

        snapshot_date = snapshot_date or datetime.date.today()
        result = self.get_nft_current(
            collection_id, token_id, wallet_address, snapshot_date)

        if not result:
            return None
        (
            holder,
            data_collection_id,
            data_token_id,
            data_snapshot_date,
            interest,
            principal,
            updateAppliedId,
            hold_days,
        ) = result

        return {
            "datetime": str(data_snapshot_date),
            "paid": False,
            "interestRate": interest,
            "principal": principal,
            "updateAppliedId": updateAppliedId,
            "holdDaysInCurrentMonth": hold_days,
        }

    def get_nft_current(
        self, collection_id, token_id, wallet_address, snapshot_date=None
    ):
        snapshot_date = snapshot_date or datetime.date.today()
        with self.connection.cursor() as cursor:

            self._execute_query(
                cursor=cursor,
                query_template=self.get_nft_current_query_template,
                collection_id=collection_id,
                token_id=token_id,
                wallet_address=wallet_address,
                snapshot_date=str(snapshot_date)
            )

            return cursor.fetchone()

    def get_nfts_summary_by_wallet(
        self, collection_id, wallet_address, snapshot_date=None
    ):
        snapshot_date = snapshot_date or datetime.date.today()
        result = self.get_nfts_summary_by_wallet(
            collection_id, wallet_address, snapshot_date)

        if not result:
            return None

        holder, sum_InterestEarnedInMonth, count_TokenId = result
        return {
            "walletAddress": holder,
            "totalEarnInCurrentMonth": sum_InterestEarnedInMonth,
            "totalNftsInCurrentMonth": count_TokenId,
        }

    get_nfts_summary_by_wallet_query_template = f'''
        SELECT Holder, SUM(InterestEarnedInMonth), COUNT(TokenId)
        FROM {NFT_HOLDER_BY_DATE_TABLE_NAME} 
        WHERE CollectionId = $collection_id
        AND Holder = '$wallet_address' 
        AND SnapshotDate = '$snapshot_date)';
    '''

    def get_nfts_summary_by_wallet(
        self, collection_id, wallet_address, snapshot_date=None
    ):
        snapshot_date = snapshot_date or datetime.date.today()
        with self.connection.cursor() as cursor:

            self._execute_query(
                cursor=cursor,
                query_template=self.get_nfts_summary_by_wallet_query_template,
                collection_id=collection_id,
                wallet_address=wallet_address,
                snapshot_date=str(snapshot_date)
            )

            return cursor.fetchone()

    get_nfts_summary_by_wallet_query_template = f'''
        SELECT SUM(InterestEarnedInMonth), kyc 
        FROM {NFT_HOLDER_BY_DATE_TABLE_NAME} hbd 
        INNER JOIN {WALLET_TABLE_NAME} w ON w.Address = hbd.Holder  
        WHERE CollectionId = $collection_id 
        AND Holder = '$wallet_address' 
        AND SnapshotDate = '$snapshot_date';
    '''

    def get_wallet_nfts(self, collection_id, wallet_address, snapshot_date=None):
        snapshot_date = snapshot_date or datetime.date.today()
        result = self.get_wallet_nfts(
            collection_id, wallet_address, snapshot_date)
        if not result:
            return None

        totalEarnInCurrentMonth, kyc = result

        if not totalEarnInCurrentMonth:
            return None

        data = {
            "totalEarnInCurrentMonth": totalEarnInCurrentMonth,
            "kyc": kyc == b'\x01',
            "walletAddress": wallet_address
        }

        return data

    def get_wallet_nfts(self, collection_id, wallet_address, snapshot_date=None):
        snapshot_date = snapshot_date or datetime.date.today()
        with self.connection.cursor() as cursor:

            self._execute_query(
                cursor=cursor,
                query_template=self.get_nfts_summary_by_wallet_query_template,
                collection_id=collection_id,
                wallet_address=wallet_address,
                snapshot_date=str(snapshot_date)
            )

            return cursor.fetchone()

    def fetch_closest_update(self, today, collection_id):
        self.cursor.execute(
            "SELECT FromDate,Principal,Interest,Id FROM NVC.CollectionUpdate "
            + f"WHERE (TIMESTAMPDIFF(day, FromDate, '{today}') ) >= 0 AND CollectionId = {str(collection_id)} "
            + "ORDER BY FromDate DESC LIMIT 1 ;"
        )
        result = self.cursor.fetchall()
        self.connection.close()
        return (result[0][0], result[0][1], result[0][2], result[0][3])

    def get_unique_holder(self, collection_id, snapshot_date=None):
        snapshot_date = snapshot_date or datetime.date.today()
        self.cursor.execute(
            "SELECT count(distinct Holder) FROM NVC.HolderByDate "
            + f"WHERE SnapshotDate = '{snapshot_date}' AND Holding = 1 AND CollectionId = {collection_id};"
        )
        result = self.cursor.fetchone()
        self.connection.close()
        return result[0]

    def get_total_pay(self, collection_id, snapshot_date=None):
        snapshot_date = snapshot_date or datetime.date.today()
        self.cursor.execute(
            "SELECT sum(InterestEarned) FROM NVC.HolderByDate "
            + f"WHERE SnapshotDate = '{snapshot_date}' AND CollectionId = {collection_id};"
        )
        result = self.cursor.fetchone()
        self.connection.close()
        return result[0]

    def get_reset_day(self, collection_id, snapshot_date=None):
        snapshot_date = snapshot_date or datetime.date.today()
        self.cursor.execute(
            "SELECT FromDate FROM NVC.CollectionUpdate "
            + f"WHERE (TIMESTAMPDIFF(day, FromDate, '{snapshot_date}') ) <= 0 AND CollectionId = {collection_id} AND Type = 'Update' "
            + "ORDER BY FromDate ASC LIMIT 1"
        )
        result = self.cursor.fetchone()
        self.connection.close()
        return result[0]

    def get_report_data(self, collection_id, snapshot_date=None):
        snapshot_date = snapshot_date or datetime.date.today()
        self.cursor.execute(
            "SELECT Principal, Interest, TotalSupply, FromDate "
            + "FROM NVC.CollectionUpdate cu "
            + "INNER JOIN NVC.Collection c ON cu.CollectionId = c.Id "
            + f"WHERE (TIMESTAMPDIFF(day, FromDate, '{snapshot_date}') ) < 0 AND CollectionId = {collection_id} AND Type = 'Update' "
            + "ORDER BY FromDate ASC LIMIT 1 ;"
        )
        result = self.cursor.fetchall()
        self.connection.close()
        return (result[0][0], result[0][1], result[0][2], result[0][3])

    def get_reset_day(self, collection_id, snapshot_date=None):
        snapshot_date = snapshot_date or datetime.date.today()
        self.cursor.execute(
            "SELECT FromDate FROM NVC.CollectionUpdate "
            + f"WHERE (TIMESTAMPDIFF(day, FromDate, '{snapshot_date}') ) <= 0 AND CollectionId = {collection_id} AND Type = 'Update' "
            + "ORDER BY FromDate ASC LIMIT 1"
        )
        result = self.cursor.fetchone()
        self.connection.close()
        return result[0]
