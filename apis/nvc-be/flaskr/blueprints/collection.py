import datetime
from turtle import left
from flask import Blueprint,  request
import json
import jwt
from flaskr.mysql import SqlConnector
from web3 import Web3
collection = Blueprint("collections", __name__, url_prefix="/api/collections")

admins = [Web3.toChecksumAddress("0x811a7c9334966401C22B79a55B6aCE749004D543"), Web3.toChecksumAddress(
    "0xF8eD875352236eF987a9c8855e9a6c0FE9B541db")]


@collection.route("/<id>")
def index(id):
    sql = SqlConnector()
    collection = sql.get_collection_by_id(id)
    if collection:
        return collection, 200
    else:
        return "Not found", 404


daily_data = {}
prev_day = None


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
    if(Web3.toChecksumAddress(payload["wallet"]) not in admins):
        return {'message': 'Unauthorized.'}, 403

    global prev_day
    global daily_data
    print(prev_day)
    if not prev_day or prev_day != datetime.date.today():
        sql = SqlConnector()
        unique_holders = sql.get_unique_holder(id)
        sql = SqlConnector()
        total_pay = sql.get_total_pay(id)
        sql = SqlConnector()
        (principal, interest, total_supply, from_date) = sql.get_report_data(
            id
        )
        sql = SqlConnector()
        reset_day = sql.get_reset_day(id)
        print(reset_day)
        days_left = reset_day - datetime.date.today()
        print(interest)
        estimate = (total_supply * principal *
                    interest / 100 / 365 * days_left.days)
        daily_data = {
            "uniqueHolders": unique_holders,
            "totalPay": total_pay,
            "estimate": estimate,
        }
    prev_day = datetime.date.today()
    return daily_data


@collection.route("/<collection_id>/nfts/<nft_id>")
def nft_detail(collection_id, nft_id):

    wallet_address = request.args.get('walletAddress')
    snapshot_date = request.args.get('snapshotDate')
    if(not snapshot_date):
        snapshot_date = datetime.date.today()
    print(f"snapshot_dateasdasd {str(snapshot_date)}")
    sql = SqlConnector()
    earnings = sql.get_nft_history(
        collection_id, nft_id, wallet_address, snapshot_date)
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
    sql = SqlConnector()
    data = sql.get_wallet_nfts(collection_id, wallet_address)
    return (data, 200) if data else ("404", 404)


@collection.route("/<collection_id>/nfts/<nft_id>/current")
def nft_detail_cur(collection_id, nft_id):
    wallet_address = request.args.get('walletAddress')
    snapshot_date = request.args.get('snapshotDate')
    if(not snapshot_date):
        snapshot_date = datetime.date.today()

    sql = SqlConnector()
    data = sql.get_nft_current(
        collection_id, nft_id, wallet_address, snapshot_date)
    # if earnings is None:
    #     return "Not found", 404
    if(not data):
        return "", 404
    return data
