import datetime
from turtle import left
from flask import Blueprint,  request
import json

from flaskr.mysql import SqlConnector

collection = Blueprint("collections", __name__, url_prefix="/api/collections")


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
