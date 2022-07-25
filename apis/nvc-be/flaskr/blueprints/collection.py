import datetime
from flask import current_app, Blueprint,  request
import json
import jwt
from web3 import Web3
# import sys
# print([ key for key in sys.modules.keys() ])
from flaskr.business_layer.collection import CollectionBusinessLayer
collection = Blueprint("collections", __name__, url_prefix="/api/collections")

# daily_data = {}
# prev_day = None


@collection.route("/<id>")
def index(id):
    handler = CollectionBusinessLayer(current_app.config["DATABASE"])
    collection = handler.get_collection_with_updates_by_id(id)

    if collection:
        return collection, 200
    else:
        return "Not found", 404

@collection.route("/<id>/interest-report")
def collection_interest_report(id):
    '''
    data = {
        data:[
            {
                "wallet":"0xasd",
                "interest:1.1
            }
        ],
        parsed:""
    }
    '''
    
    snapshot_date = request.args.get('snapshotDate')
    if(not snapshot_date):
        snapshot_date = datetime.date.today()

    handler = CollectionBusinessLayer(current_app.config["DATABASE"])

    data= handler.get_collection_interest_report(id,snapshot_date)


    return data,200

@collection.route("/<id>/report")
def collection_report(id):
    authorization = request.headers.get('Authorization')
    if(not authorization):
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
    if(Web3.toChecksumAddress(payload["wallet"]) not in current_app.config["ADMIN_WALLETS"]):
        return {'message': 'Unauthorized.'}, 403

    # global prev_day
    # global daily_data
    # if not prev_day or prev_day != datetime.date.today():

    snapshot_date = request.args.get('snapshotDate')
    if(not snapshot_date):
        snapshot_date = datetime.date.today()

    handler = CollectionBusinessLayer(current_app.config["DATABASE"])
    unique_holders = handler.get_unique_holder(id, snapshot_date)

    total_pay = handler.get_total_pay(id, snapshot_date)

    (principal, interest, total_supply, from_date) = handler.get_report_data(
        id
    )

    reset_day = handler.get_reset_day(id, snapshot_date)
    print(reset_day)
    days_left = reset_day - snapshot_date

    estimate = (total_supply * principal *
                interest / 100 / 365 * days_left.days)
    daily_data = {
        "uniqueHolders": unique_holders,
        "totalPay": total_pay,
        "estimate": estimate,
    }
    # prev_day = datetime.date.today()
    return daily_data


@collection.route("/<collection_id>/nfts/<nft_id>")
def nft_detail(collection_id, nft_id):

    wallet_address = request.args.get('walletAddress')

    handler = CollectionBusinessLayer(current_app.config["DATABASE"])
    earnings = handler.get_nft_history(
        collection_id, nft_id, wallet_address)
    print(json.dumps(earnings))
    # if earnings is None:
    #     return "Not found", 404

    return {
        "wallet": wallet_address,
        "tokenId": nft_id,
        "collectionId": collection_id,
        "earnings": earnings
    }


@collection.route("/<collection_id>/wallets/<wallet_address>")
def wallet_detail(collection_id, wallet_address):
    snapshot_date = request.args.get('snapshotDate')
    if(not snapshot_date):
        snapshot_date = datetime.date.today()

    handler = CollectionBusinessLayer(current_app.config["DATABASE"])
    data = handler.get_wallet_nfts(
        collection_id, wallet_address, snapshot_date)
    return (data, 200) if data else ("404", 404)


@collection.route("/<collection_id>/nfts/<nft_id>/current")
def nft_detail_cur(collection_id, nft_id):
    wallet_address = request.args.get('walletAddress')
    snapshot_date = request.args.get('snapshotDate')
    if(not snapshot_date):
        snapshot_date = datetime.date.today()

    handler = CollectionBusinessLayer(current_app.config["DATABASE"])
    data = handler.get_nft_current(
        collection_id, nft_id, wallet_address, snapshot_date)
    # if earnings is None:
    #     return "Not found", 404
    if(not data):
        return "", 404
    return data
