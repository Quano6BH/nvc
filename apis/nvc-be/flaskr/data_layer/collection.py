import MySQLdb
from string import Template
from .base import BaseDataLayer
class CollectionDataLayer(BaseDataLayer):

    def __init__(self, db_config):
        BaseDataLayer.__init__(self,db_config)

    get_collection_with_updates_by_id_query_template = f'''
        SELECT c.Id, StartDate, EndDate, Ipfs, TotalSupply,Address,  
        NetworkId, Principal, Interest, FromDate, Type, Message, BuyBack, cu.Id 
        FROM {BaseDataLayer.COLLECTION_TABLE_NAME} c 
        INNER JOIN {BaseDataLayer.COLLECTION_UPDATE_TABLE_NAME} cu
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
        FROM {BaseDataLayer.NFT_HOLDER_BY_MONTH_TABLE_NAME} hbm 
            INNER JOIN {BaseDataLayer.NFT_HOLDER_BY_DATE_TABLE_NAME} hbd 
            ON hbm.CollectionId = hbd.CollectionId 
            AND hbm.Holder = hbd.Holder 
            AND hbm.ResetDate = hbd.SnapshotDate 
            INNER JOIN {BaseDataLayer.COLLECTION_UPDATE_TABLE_NAME} cu 
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

    get_collection_latest_holder_by_month_query = f'''
        SELECT ResetDate
        FROM {BaseDataLayer.NFT_HOLDER_BY_MONTH_TABLE_NAME}
        WHERE ResetDate <= '$snapshot_date' AND CollectionId = $collection_id
        ORDER BY ResetDate DESC LIMIT 1

    '''
    def get_collection_latest_holder_by_month(self, collection_id, snapshot_date):

        with self.create_db_connection(self.db_config) as db_connection:
            with db_connection.cursor() as cursor:

                self._execute_query(
                    cursor=cursor,
                    query_template=self.get_collection_latest_holder_by_month_query,
                    collection_id=collection_id,
                    snapshot_date=str(snapshot_date)
                )

                return cursor.fetchone()

    get_collection_interest_report_query = f'''
        SELECT Holder, InterestEarnedInMonth
        FROM {BaseDataLayer.NFT_HOLDER_BY_DATE_TABLE_NAME}
        WHERE SnapshotDate = '$snapshot_date' AND CollectionId = $collection_id
        

    '''
    def get_collection_interest_report(self, collection_id, snapshot_date):
        with self.create_db_connection(self.db_config) as db_connection:
            with db_connection.cursor() as cursor:

                self._execute_query(
                    cursor=cursor,
                    query_template=self.get_collection_interest_report_query,
                    collection_id=collection_id,
                    snapshot_date=str(snapshot_date)
                )

                return cursor.fetchall()



    get_nft_current_query_template = f'''
        SELECT hbd.Holder, hbd.CollectionId, hbd.TokenId, SnapshotDate, 
                     cu.Interest, cu.Principal, hbd.UpdateAppliedId, hbd.HoldDaysinMonth 
        FROM {BaseDataLayer.NFT_HOLDER_BY_DATE_TABLE_NAME} hbd 
            INNER JOIN {BaseDataLayer.COLLECTION_UPDATE_TABLE_NAME} cu 
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
        FROM {BaseDataLayer.NFT_HOLDER_BY_DATE_TABLE_NAME} 
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
        FROM {BaseDataLayer.NFT_HOLDER_BY_DATE_TABLE_NAME} hbd 
        INNER JOIN {BaseDataLayer.WALLET_TABLE_NAME} w ON w.Address = hbd.Holder  
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
        FROM {BaseDataLayer.NFT_HOLDER_BY_DATE_TABLE_NAME} 
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
        FROM {BaseDataLayer.NFT_HOLDER_BY_DATE_TABLE_NAME}
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
        FROM {BaseDataLayer.COLLECTION_UPDATE_TABLE_NAME} cu 
            INNER JOIN {BaseDataLayer.COLLECTION_TABLE_NAME} c 
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
        FROM {BaseDataLayer.COLLECTION_UPDATE_TABLE_NAME}
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
