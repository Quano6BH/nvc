from flask import current_app, Blueprint
wallet = Blueprint('wallets', __name__, url_prefix='/wallets')

@wallet.route('/<address>')
def index(address):
    return {
        "id":1,
        "start_date":"31/05/2022",
        "end_date":"31/05/2023",
        "ipfs":"ipfs://",
        "total_supply":10000,
        "address":"0xasdasdasdasd",
        "network_id":3,
        
        }
