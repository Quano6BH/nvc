from flask import current_app, Blueprint, request
collection = Blueprint('collections', __name__, url_prefix='/collections')


@collection.route('/<id>')
def index(id):
    return {
        "id": id,
        "start_date": "2022-05-31T23:50:55",
        "end_date": "2023-05-31T23:50:55",
        "ipfs": "ipfs://",
        "total_supply": 10000,
        "address": "0xasdasdasdasd",
        "network_id": 3,
    }


@collection.route("/collections/<id>/report")
def collection_report(id):
    return {

    }


@collection.route("/collections/<collection_id>/nfts/<nft_id>")
def collection_report(collection_id, nft_id):
    wallet_address = request.args.get('wallet')
    return {

    }
