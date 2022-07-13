import MySQLdb
from string import Template


class CollectionDataLayer:
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

    get_collection_with_updates_by_id_query_template = f'''
        SELECT c.Id, StartDate, EndDate, Ipfs, TotalSupply,Address,  
        NetworkId, Principal, Interest, FromDate, Type, Message, BuyBack, cu.Id 
        FROM {COLLECTION_TABLE_NAME} c 
        INNER JOIN {COLLECTION_UPDATE_TABLE_NAME} cu
        ON  c.Id = cu.CollectionId 
        WHERE c.Id = $collection_id;
    '''

    def get_collection_with_updates_by_id(self, collection_id):
        with self.create_db_connection(self.db_config) as db_connection:
            with db_connection.cursor() as cursor:
                self._execute_query(
                    cursor=cursor,
                    query_template=self.get_collection_with_updates_by_id_query_template,
                    collection_id=collection_id
                )

                return cursor.fetchall()

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
        with self.create_db_connection(self.db_config) as db_connection:
            with db_connection.cursor() as cursor:

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
        self, collection_id, token_id, wallet_address, snapshot_date
    ):
        with self.create_db_connection(self.db_config) as db_connection:
            with db_connection.cursor() as cursor:

                self._execute_query(
                    cursor=cursor,
                    query_template=self.get_nft_current_query_template,
                    collection_id=collection_id,
                    token_id=token_id,
                    wallet_address=wallet_address,
                    snapshot_date=str(snapshot_date)
                )

                return cursor.fetchone()

    get_nfts_summary_by_wallet_query_template = f'''
        SELECT Holder, SUM(InterestEarnedInMonth), COUNT(TokenId)
        FROM {NFT_HOLDER_BY_DATE_TABLE_NAME} 
        WHERE CollectionId = $collection_id
        AND Holder = '$wallet_address' 
        AND SnapshotDate = '$snapshot_date)';
    '''

    def get_nfts_summary_by_wallet(
        self, collection_id, wallet_address, snapshot_date
    ):
        with self.create_db_connection(self.db_config) as db_connection:
            with db_connection.cursor() as cursor:

                self._execute_query(
                    cursor=cursor,
                    query_template=self.get_nfts_summary_by_wallet_query_template,
                    collection_id=collection_id,
                    wallet_address=wallet_address,
                    snapshot_date=str(snapshot_date)
                )

                return cursor.fetchone()

    get_wallet_nfts_query_template = f'''
        SELECT SUM(InterestEarnedInMonth), kyc 
        FROM {NFT_HOLDER_BY_DATE_TABLE_NAME} hbd 
        INNER JOIN {WALLET_TABLE_NAME} w ON w.Address = hbd.Holder  
        WHERE CollectionId = $collection_id 
        AND Holder = '$wallet_address' 
        AND SnapshotDate = '$snapshot_date';
    '''

    def get_wallet_nfts(self, collection_id, wallet_address, snapshot_date):
        with self.create_db_connection(self.db_config) as db_connection:
            with db_connection.cursor() as cursor:

                self._execute_query(
                    cursor=cursor,
                    query_template=self.get_wallet_nfts_query_template,
                    collection_id=collection_id,
                    wallet_address=wallet_address,
                    snapshot_date=str(snapshot_date)
                )

                return cursor.fetchone()

    get_unique_holder_query_template = f'''
        SELECT count(distinct Holder) 
        FROM {NFT_HOLDER_BY_DATE_TABLE_NAME} 
        WHERE SnapshotDate = '$snapshot_date' 
        AND Holding = 1 
        AND CollectionId = $collection_id;
    '''

    def get_unique_holder(self, collection_id, snapshot_date):
        with self.create_db_connection(self.db_config) as db_connection:
            with db_connection.cursor() as cursor:

                self._execute_query(
                    cursor=cursor,
                    query_template=self.get_unique_holder_query_template,
                    collection_id=collection_id,
                    snapshot_date=str(snapshot_date)
                )

                return cursor.fetchone()

    get_total_pay_query_template = f'''
        SELECT sum(InterestEarned) 
        FROM {NFT_HOLDER_BY_DATE_TABLE_NAME}
        WHERE SnapshotDate = '$snapshot_date' 
        AND CollectionId = $collection_id;
        
    '''

    def get_total_pay(self, collection_id, snapshot_date):
        with self.create_db_connection(self.db_config) as db_connection:
            with db_connection.cursor() as cursor:

                self._execute_query(
                    cursor=cursor,
                    query_template=self.get_total_pay_query_template,
                    collection_id=collection_id,
                    snapshot_date=str(snapshot_date)
                )

                return cursor.fetchone()


    get_report_data_query_template = f'''
        SELECT Principal, Interest, TotalSupply, FromDate 
        FROM {COLLECTION_UPDATE_TABLE_NAME} cu 
            INNER JOIN {COLLECTION_TABLE_NAME} c 
            ON cu.CollectionId = c.Id 
        WHERE (TIMESTAMPDIFF(day, FromDate, '$snapshot_date') ) < 0 
        AND CollectionId = $collection_id AND Type = 'Update' 
        ORDER BY FromDate ASC LIMIT 1 ;
    '''

    def get_report_data(self, collection_id, snapshot_date):
        with self.create_db_connection(self.db_config) as db_connection:
            with db_connection.cursor() as cursor:

                self._execute_query(
                    cursor=cursor,
                    query_template=self.get_report_data_query_template,
                    collection_id=collection_id,
                    snapshot_date=str(snapshot_date)
                )

                return cursor.fetchall()

    get_reset_day_query_template = f'''
        SELECT FromDate 
        FROM {COLLECTION_UPDATE_TABLE_NAME}
        WHERE (TIMESTAMPDIFF(day, FromDate, '$snapshot_date') ) <= 0 
        AND CollectionId = $collection_id 
        AND Type = 'Update' 
        ORDER BY FromDate ASC LIMIT 1
    '''

    def get_reset_day(self, collection_id, snapshot_date=None):

        with self.create_db_connection(self.db_config) as db_connection:
            with db_connection.cursor() as cursor:

                self._execute_query(
                    cursor=cursor,
                    query_template=self.get_reset_day_query_template,
                    collection_id=collection_id,
                    snapshot_date=str(snapshot_date)
                )

                return cursor.fetchone()
