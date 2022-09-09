
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
    """Return detail data of an nft by wallet.
    ---
    parameters:
      - in: path
        name: wallet_address
        schema:
          type: string
        required: true
      - in: query
        name: tokenId
        schema:
          type: int
        required: true
      - in: query
        name: collectionId
        schema:
          type: int
        required: true
    responses:
      200:
        description: Detail data of an nft by wallet.
        examples:
          application/json:
            {
                "data": {
            "walletAddress": 0xF2Ccf89d5C92036A8075F6da96E1bb970969AA47,
            "nftId": 0,
            "collectionId": 0,
            "datetime": 2022-08-12,
            "history": {
                    "datetime": 2022-08-12,
                    "paid": 1,
                    "interestRate": 10%,
                    "principal": 1000,
                    "updateAppliedId": 1,
                    "holdDays": 10,
                    "interestEarned": 5,
                },
            "current":  {
            "datetime": 2022-08-12,
            "interestRate": 10%,
            "principal": 1000,
            "updateAppliedId": 1,
            "holdDays": 10,
            "interestEarned": 10,
        }
        }
            }
    """
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


# @wallet.route('<address>', methods=["PATCH"])
# def update(address):
#     """Update kyc of wallet
#     ---
#     parameters:
#       - in: path
#         name: address
#         schema:
#           type: string
#         required: true
#     responses:
#       200:
#         description: update kyc status 
#         examples:
#           200
#     """
#     body = request.get_json()
#     kyc = body["kyc"]
#     handler = WalletBusinessLayer(current_app.config["DATABASE"])

#     handler.update_wallet_kyc(address, kyc)

#     return "", 200


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
    # authorization = request.headers.get('Authorization')
    # if (not authorization):
    #     return {'message': 'Unauthorized.'}, 403

    # authorization = authorization.replace(authorization[0:7], '')
    # payload = {}
    # try:

    #     payload = jwt.decode(authorization, "secret", algorithms=["HS256"])
    # except jwt.ExpiredSignatureError:
    #     return {'message': 'Token expired, log in again'}, 403
    # except jwt.InvalidTokenError:
    #     return {'message': 'Invalid token. Please log in again.'}, 403

    # # print(payload)
    # if (Web3.toChecksumAddress(payload["wallet"]) not in current_app.config["ADMIN_WALLETS"]):
    #     return {'message': 'Unauthorized.'}, 403

    body = request.get_json()
    kyc = body["kyc"]
    addresses = body["addresses"]
    handler = WalletBusinessLayer(current_app.config["DATABASE"])

    handler.update_wallets_kyc(addresses, kyc)

    return "", 200


@wallet.route("/<wallet_address>",methods=["GET"])
def wallet_detail(wallet_address):
    """Return wallet info in one collection.
    ---
    parameters:
      - in: path
        name: wallet_address
        schema:
          type: string
        required: true
    responses:
      200:
        description: wallet info in one collection
        examples:
          application/json:
            {
               "kyc": 1,
            "walletAddress": 0x0013C382001DF4022FE14814a865cEF7Fb814e14
            }
            
    """

    # date_time = request.args.get('datetime')
    # if (not date_time):

    handler = WalletBusinessLayer(current_app.config["DATABASE"])
    data = handler.get_wallet_info(
        wallet_address)

    return ({"data": data}, 200) if data else ("404", 404)
