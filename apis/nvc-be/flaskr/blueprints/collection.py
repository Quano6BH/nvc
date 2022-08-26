import datetime
from functools import wraps
from flask import current_app, Blueprint, jsonify, make_response,  request
import json
import jwt
from web3 import Web3
from flaskr.cache import cache
from flaskr.business_layer.collection import CollectionBusinessLayer
collection = Blueprint("collections", __name__, url_prefix="/api/collections")



def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None
        if 'Authorization' in request.headers:
            token = request.headers.get('Authorization')

        if (not token):
            return make_response(jsonify({"message": "A valid token is missing!"}), 401)

        token = token.replace(token[0:7], '')
        payload = {}
        try:

            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return make_response(jsonify({'message': 'Token expired, log in again'}), 401)
        except jwt.InvalidTokenError:
            return make_response(jsonify({'message': 'Invalid token. Please log in again.'}), 401)

        if (Web3.toChecksumAddress(payload["wallet"]) not in current_app.config["ADMIN_WALLETS"]):
            return make_response(jsonify({'message': 'Unauthorized.'}), 401)

        return f(*args, **kwargs)
    return decorator


@collection.route("/")
def index():
    handler = CollectionBusinessLayer(current_app.config["DATABASE"])
    collections = handler.get_collections()

    if collections:
        return {"data": collections}, 200
    else:
        return "Not found", 404


@collection.route("/<id>")
def get_collection_by_id(id):
    handler = CollectionBusinessLayer(current_app.config["DATABASE"])
    collection = handler.get_collection_with_updates_by_id(id)

    if collection:
        return {"data": collection}, 200
    else:
        return "Not found", 404


@collection.route("/<collection_id>/nfts/<nft_id>", methods=["GET"])
def get_nft_interest_history(collection_id, nft_id):

    # if (not snapshot_date):
    snapshot_date = datetime.date.today()

    handler = CollectionBusinessLayer(current_app.config["DATABASE"])
    history = handler.get_nft_interest_history(
        collection_id, nft_id, snapshot_date)

    return {
        "data": {
            "tokenId": nft_id,
            "collectionId": collection_id,
            "history": history
        }
    }



COLLECTION_REPORT_CACHE_KEY = "collection_report"


@collection.route("/<id>/report")
@token_required
def collection_report(id):

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

    date_time = datetime.date.today()
    # if (not date_time):
    #     date_time = datetime.date.today()
    # else:
    #     date_time = datetime.datetime.strptime(date_time, '%Y-%m-%d').date()
    handler = CollectionBusinessLayer(current_app.config["DATABASE"])
    unique_holders = handler.get_unique_holder(id, date_time)

    total_pay = handler.get_total_pay(id, date_time)

    (principal, interest, total_supply, _) = handler.get_report_data(
        id
    )

    reset_day = handler.get_reset_day(id, date_time)

    days_left = reset_day - date_time

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

    return daily_data
