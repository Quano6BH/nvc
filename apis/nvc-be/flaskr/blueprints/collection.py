import datetime
from flask import current_app, Blueprint, jsonify, request

from flaskr.mysql import SqlConnector
collection = Blueprint('collections', __name__, url_prefix='/collections')


@collection.route('/<id>')
def index(id):
    sql = SqlConnector()
    collection = sql.get_collection_by_id(id)
    if collection:
        return collection,200
    else:
        return "Not found", 404


@collection.route("/<id>/report")
def collection_report(id):
    return {
        "uniqueHolders": 12,
        "totalPay": 123999,
        "estimate": 123991,
    }


@collection.route("/<collection_id>/nfts/<nft_id>")
def nft_detail(collection_id, nft_id):
    wallet_address = request.args.get('walletAddress')
    snapshot_date = request.args.get('snapshotDate')
    if(not snapshot_date):
        snapshot_date= datetime.date.today()

    sql = SqlConnector()
    nft_prev_months = sql.get_nft_detail_prev_month(
        collection_id, nft_id, wallet_address, snapshot_date)
    if nft_prev_months is None:
        return "Not found", 404

    sql = SqlConnector()
    nft_current = sql.get_nft_detail_current_month(
        collection_id, nft_id, wallet_address)
    if nft_current is None:
        return "Not found", 404

    nft_prev_months["holdDaysInCurrentMonth"] = nft_current["hold_days_in_month"]
    nft_prev_months["earnings"].append({
        "datetime": str(nft_current["snapshot_date"]),
        "collectionId": nft_current["collection_id"],
        "interestEarned": nft_current["interest_earned_in_month"],
    })
    return nft_prev_months
