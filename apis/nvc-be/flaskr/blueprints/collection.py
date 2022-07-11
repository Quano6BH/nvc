import datetime
from turtle import left
from flask import current_app, Blueprint, jsonify, request
from flaskr.mysql import SqlConnector


collection = Blueprint("collections", __name__, url_prefix="/collections")


@collection.route("/<id>")
def index(id):
    sql = SqlConnector()
    collection = sql.get_collection_by_id(id)
    if collection:
        return collection, 200
    else:
        return "Not found", 404


@collection.route("/<id>/report")
def collection_report(id):
    sql = SqlConnector()
    unique_holders = sql.get_unique_holder(id, "2022-07-09")
    sql = SqlConnector()
    total_pay = sql.get_total_pay(id, "2022-07-09")
    sql = SqlConnector()
    (principal, interest, total_supply, from_date) = sql.get_report_data(
        id, "2022-07-09"
    )
    sql = SqlConnector()
    reset_day = sql.get_reset_day(id, "2022-07-09")
    print(reset_day)
    days_left = reset_day - datetime.date.today()
    print(days_left.days - 1)
    estimate = total_supply * principal * interest / 100 / 365 * (days_left.days - 1)

    return {
        "uniqueHolders": unique_holders,
        "totalPay": total_pay,
        "estimate": estimate,
    }


@collection.route("/<collection_id>/nfts/<nft_id>")
def nft_detail(collection_id, nft_id):
    wallet_address = request.args.get("walletAddress")
    snapshot_date = request.args.get("snapshotDate")
    if not snapshot_date:
        snapshot_date = datetime.date.today()

    sql = SqlConnector()
    nft_prev_months = sql.get_nft_detail_prev_month(
        collection_id, nft_id, wallet_address, snapshot_date
    )
    if nft_prev_months is None:
        return "Not found", 404

    sql = SqlConnector()
    nft_current = sql.get_nft_detail_current_month(
        collection_id, nft_id, wallet_address
    )
    if nft_current is None:
        return "Not found", 404

    nft_prev_months["holdDaysInCurrentMonth"] = nft_current["hold_days_in_month"]
    nft_prev_months["earnings"].append(
        {
            "datetime": str(nft_current["snapshot_date"]),
            "collectionId": nft_current["collection_id"],
            "interestEarned": nft_current["interest_earned_in_month"],
        }
    )
    return nft_prev_months
