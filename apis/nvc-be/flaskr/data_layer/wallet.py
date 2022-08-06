from ntpath import join
import MySQLdb
from string import Template
from .base import BaseDataLayer


class WalletDataLayer(BaseDataLayer):

    def __init__(self, db_config):
        BaseDataLayer.__init__(self,db_config)

    def create_db_connection(self, db_config):
        return MySQLdb.connect(
            host=db_config["host"],
            port=db_config["port"],
            user=db_config["username"],
            password=db_config["password"],
            database=db_config["database"],
        )

    update_wallet_kyc_query_template = f'''
        UPDATE {BaseDataLayer.WALLET_TABLE_NAME} 
        SET `Kyc` = b'$kyc' 
        WHERE (`Address` = '$address');
    '''

    def update_wallet_kyc(self, wallet_address, kyc = True):
        with self.create_db_connection(self.db_config) as db_connection:
            with db_connection.cursor() as cursor:
                self._execute_query(
                    cursor=cursor,
                    query_template=self.update_wallet_kyc_query_template,
                    kyc= 1 if kyc else 0,
                    address=wallet_address
                )
                db_connection.commit()

    update_wallets_kyc_query_template = f'''
        UPDATE {BaseDataLayer.WALLET_TABLE_NAME} 
        SET `Kyc` = b'$kyc' 
        WHERE (`Address` IN ('$addresses'));
    '''
    def update_wallets_kyc(self, wallet_addresses, kyc = True):
        with self.create_db_connection(self.db_config) as db_connection:
            with db_connection.cursor() as cursor:
                self._execute_query(
                    cursor=cursor,
                    query_template=self.update_wallets_kyc_query_template,
                    kyc= 1 if kyc else 0,
                    addresses= "','".join(wallet_addresses)
                )

                db_connection.commit()


    get_wallet_collection_info_query_template = f'''
        SELECT Address, Kyc, InterestEarnedInMonth, HoldDaysInMonth,TokenId,SnapshotDate, Holding 
        FROM {BaseDataLayer.WALLET_TABLE_NAME} w
            INNER JOIN {BaseDataLayer.NFT_HOLDER_BY_DATE_TABLE_NAME} hbd
                ON w.Address = hbd.Holder
        WHERE Address = '$wallet_address' 
        AND SnapshotDate = '$datetime'
        AND CollectionId = $collection_id;
    '''

    def get_wallet_collection_info(self, wallet_address, collection_id, datetime):
        with self.create_db_connection(self.db_config) as db_connection:
            with db_connection.cursor() as cursor:

                self._execute_query(
                    cursor=cursor,
                    query_template=self.get_wallet_collection_info_query_template,
                    wallet_address=wallet_address,
                    collection_id = collection_id,
                    datetime = str(datetime)
                )

                return cursor.fetchall()
    
    get_nft_history_of_wallet_query_template = f'''
        SELECT hbd.Holder, hbd.CollectionId, hbd.TokenId, SnapshotDate, cu.Interest, cu.Principal, 
            hbd.UpdateAppliedId, hbd.HoldDaysinMonth, hbd.InterestEarnedInMonth, hbd.Paid 
        FROM {BaseDataLayer.NFT_HOLDER_BY_MONTH_TABLE_NAME} hbm 
            INNER JOIN {BaseDataLayer.NFT_HOLDER_BY_DATE_TABLE_NAME} hbd 
                ON hbm.CollectionId = hbd.CollectionId 
                AND hbm.Holder = hbd.Holder 
                AND hbm.ResetDate = hbd.SnapshotDate 
                
            INNER JOIN {BaseDataLayer.COLLECTION_UPDATE_TABLE_NAME} cu 
				ON cu.Id = hbd.UpdateAppliedId  
        
        WHERE hbd.CollectionId = $collection_id
        AND hbd.Holder = '$wallet_address' 
        AND hbd.SnapshotDate <= '$snapshot_date' 
        AND hbd.TokenId = '$token_id';
    '''

    def get_nft_history_of_wallet(
        self, wallet_address, collection_id, token_id,  snapshot_date
    ):
        with self.create_db_connection(self.db_config) as db_connection:
            with db_connection.cursor() as cursor:

                self._execute_query(
                    cursor=cursor,
                    query_template=self.get_nft_history_of_wallet_query_template,
                    collection_id=collection_id,
                    token_id=token_id,
                    wallet_address=wallet_address,
                    snapshot_date=str(snapshot_date)
                )

                return cursor.fetchall()

    get_nft_detail_in_current_month_of_wallet_query_template = f'''
        SELECT hbd.Holder, hbd.CollectionId, hbd.TokenId, SnapshotDate, cu.Interest, cu.Principal, 
            hbd.UpdateAppliedId, hbd.HoldDaysinMonth, hbd.InterestEarnedInMonth
        FROM {BaseDataLayer.NFT_HOLDER_BY_DATE_TABLE_NAME} hbd 
                
            INNER JOIN CollectionUpdate cu 
				ON cu.Id = hbd.UpdateAppliedId  
        WHERE hbd.CollectionId = $collection_id
        AND hbd.Holder = '$wallet_address' 
        AND hbd.SnapshotDate = '$snapshot_date' 
        AND hbd.TokenId = '$token_id';
    '''

    def get_nft_detail_in_current_month_of_wallet(
        self, wallet_address, collection_id, token_id,  snapshot_date
    ):
        with self.create_db_connection(self.db_config) as db_connection:
            with db_connection.cursor() as cursor:

                self._execute_query(
                    cursor=cursor,
                    query_template=self.get_nft_detail_in_current_month_of_wallet_query_template,
                    collection_id=collection_id,
                    token_id=token_id,
                    wallet_address=wallet_address,
                    snapshot_date=str(snapshot_date)
                )

                return cursor.fetchone()
