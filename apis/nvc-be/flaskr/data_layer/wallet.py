from ntpath import join
import MySQLdb
from string import Template
from .base import BaseDataLayer


class WalletDataLayer(BaseDataLayer):

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

