from flask import current_app, Blueprint
wallet = Blueprint('wallets', __name__, url_prefix='/api/wallets')


@wallet.route('/<address>')
def index(address):
    # data= sql.get_wallet_nfts()
    return {
        "walletAddress": address,
        "totalEarnInCurrentMonth": 12300,
        "kyc": True
    }
