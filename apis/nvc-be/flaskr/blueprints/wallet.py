from flask import current_app, Blueprint
wallet = Blueprint('wallets', __name__, url_prefix='/wallets')


@wallet.route('/<address>')
def index(address):
    return {
        "walletAddress": address,
        "totalEarnInCurrentMonth": 12300,
    }
