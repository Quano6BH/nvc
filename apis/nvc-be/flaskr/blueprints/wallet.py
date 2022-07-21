
import datetime
from flask import request, Blueprint, current_app
from eth_account.messages import encode_defunct
from web3.auto import w3
from web3 import Web3
from flaskr.business_layer.wallet import WalletBusinessLayer
wallet = Blueprint('wallet', __name__,
                   url_prefix='/api/wallets')


@wallet.route('<address>', methods=["PATCH"])
def update(address):
    '''
    Request: {
        "kyc": True
    }
    '''
    body = request.get_json()
    kyc = body["kyc"]
    handler = WalletBusinessLayer(current_app.config["DATABASE"])

    handler.update_wallet_kyc(address, kyc)

    return "", 200


@wallet.route('', methods=["PATCH"])
def index():
    '''
    Request: {
        "kyc": True,
        "addresses":[
            "0x000B8568aFa6F63969018c57162C5d526a703824",
            "0x0013C382001DF4022FE14814a865cEF7Fb814e14"
        ]
    }
    '''
    body = request.get_json()
    kyc = body["kyc"]
    addresses = body["addresses"]
    handler = WalletBusinessLayer(current_app.config["DATABASE"])

    handler.update_wallets_kyc(addresses, kyc)

    return "", 200
