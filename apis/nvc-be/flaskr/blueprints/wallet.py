
import datetime
from flask import request, Blueprint, current_app
from eth_account.messages import encode_defunct
import jwt
from web3 import Web3
from flaskr.business_layer.wallet import WalletBusinessLayer
wallet = Blueprint('wallet', __name__,
                   url_prefix='/api/wallets')


@wallet.route("/<wallet_address>/nft-detail")
def nft_detail_cur(wallet_address):
    nft_id = request.args.get('tokenId')
    collection_id = request.args.get('collectionId')
    # date_time = request.args.get('datetime')
    # if (not date_time):
    date_time = datetime.date.today()

    handler = WalletBusinessLayer(current_app.config["DATABASE"])
    history = handler.get_nft_history_of_wallet(wallet_address,
                                                collection_id, nft_id, date_time)

    current = handler.get_nft_detail_in_current_month_of_wallet(wallet_address,
                                                                collection_id, nft_id, date_time)

    return {
        "data": {
            "walletAddress": wallet_address,
            "nftId": nft_id,
            "collectionId": collection_id,
            "datetime": date_time,
            "history": history,
            "current": current
        }
    }


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
    authorization = request.headers.get('Authorization')
    if (not authorization):
        return {'message': 'Unauthorized.'}, 403

    authorization = authorization.replace(authorization[0:7], '')
    payload = {}
    try:

        payload = jwt.decode(authorization, "secret", algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return {'message': 'Token expired, log in again'}, 403
    except jwt.InvalidTokenError:
        return {'message': 'Invalid token. Please log in again.'}, 403

    # print(payload)
    if (Web3.toChecksumAddress(payload["wallet"]) not in current_app.config["ADMIN_WALLETS"]):
        return {'message': 'Unauthorized.'}, 403

    body = request.get_json()
    kyc = body["kyc"]
    addresses = body["addresses"]
    handler = WalletBusinessLayer(current_app.config["DATABASE"])

    handler.update_wallets_kyc(addresses, kyc)

    return "", 200


@wallet.route("/<wallet_address>/collections/<collection_id>")
def wallet_detail(wallet_address, collection_id):

    # date_time = request.args.get('datetime')
    # if (not date_time):
    date_time = datetime.date.today()

    handler = WalletBusinessLayer(current_app.config["DATABASE"])
    data = handler.get_wallet_collection_info(
        wallet_address, collection_id, date_time)

    return ({"data": data}, 200) if data else ("404", 404)
