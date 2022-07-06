from flask import current_app, Blueprint, request
collection = Blueprint('collections', __name__, url_prefix='/collections')


@collection.route('/<id>')
def index(id):
    return {
        "id": id,
        "startDate": "2022-07-01",
        "endDate": "2023-05-31",
        "ipfs": "asdasd",
        "totalSupply": 10000,
        "address": "0xasd",
        "networkId": 3,
        "updates": [
           {
               "principal": 10000,
               "interest": 10000,
               "from": "2023-07-01",
               "message": "This is announcement"
           }
        ]
    }


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
    return {
        "currentOwner": wallet_address,
        "holdDaysInCurrentMonth": 3,
        "collectionId": collection_id,
        "token_id": nft_id,
        "earnings": [
            {
                "datetime": "2022-07-01",
                "principal": 10000,
                "interestEarned": 0.1,
                "interestRate": 0.1
            },
            {
                "datetime": "2022-08-01",
                "principal": 10000,
                "interestEarned": 0.1,
                "interestRate": 0.1
            }
        ]
    }
