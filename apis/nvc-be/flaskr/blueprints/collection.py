import datetime
from flask import current_app, Blueprint,  request
import json
import jwt
from web3 import Web3
from flaskr.cache import cache
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
def collection_monthly_interest_snapshot(id):
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
    reset_date = handler.get_collection_latest_holder_by_month(
        id, snapshot_date)
    data = handler.get_collection_monthly_interest_snapshot(id, reset_date)

    return data, 200


COLLECTION_REPORT_CACHE_KEY = "collection_report"


@collection.route("/<id>/report")
def collection_report(id):
    '''
    collection_data = {
        "1": {
            "data":{},
            "expired_at":123
        }
    }
    '''
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

    if(Web3.toChecksumAddress(payload["wallet"]) not in current_app.config["ADMIN_WALLETS"]):
        return {'message': 'Unauthorized.'}, 403

    collection_report = cache.get(COLLECTION_REPORT_CACHE_KEY)
    is_reset_cache = request.args.get('resetCache') or False

    # check if collection_id exist in cache
    if collection_report and id in collection_report:
        collection_report_by_id = collection_report[id]

        # check for expiration, remove if expired
        if collection_report_by_id["expired_at"] >= datetime.datetime.timestamp(datetime.datetime.now()) and not is_reset_cache:
            return collection_report_by_id["data"]
        else:
            collection_report.pop(id)
            cache.set(COLLECTION_REPORT_CACHE_KEY, collection_report)

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

    if not collection_report:
        collection_report = {}
    if not id in collection_report:
        collection_report[id] = {}

    next_day = datetime.datetime.now() + datetime.timedelta(days=1)
    next_day_start = next_day.replace(hour=0, minute=0, second=0)
    collection_report[id] = {
        "expired_at": datetime.datetime.timestamp(next_day_start),
        "data": daily_data
    }

    cache.set(COLLECTION_REPORT_CACHE_KEY, collection_report)

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
