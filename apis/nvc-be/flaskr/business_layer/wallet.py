import datetime
from flaskr.data_layer.wallet import WalletDataLayer

from web3 import Web3


class WalletBusinessLayer:

    def __init__(self, db_config):
        self.data_layer = WalletDataLayer(db_config)

    def update_wallet_kyc(self, wallet_address, kyc = True):
        self.data_layer.update_wallet_kyc(wallet_address,kyc)

    
    def update_wallets_kyc(self, wallet_addresses, kyc = True):
        self.data_layer.update_wallets_kyc(wallet_addresses,kyc)
        
