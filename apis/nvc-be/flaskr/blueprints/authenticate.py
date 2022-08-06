
import datetime
from flask import request, Blueprint , current_app
from eth_account.messages import encode_defunct
from web3.auto import w3
from web3 import Web3
import uuid
import jwt
authenticate = Blueprint('authenticate', __name__,
                         url_prefix='/api/authenticate')

nonce_dict = {}
MESSAGE_TEMPLATE = "You are signing NVC Dashboard App using this nonce for address {wallet} with {nonce}."


@authenticate.route('', methods=["POST"])
def index():
    data = request.get_json()
    wallet = Web3.toChecksumAddress(data["wallet"])
    signature = data["signature"]

    if wallet not in nonce_dict.keys():
        return "Error", 404

    signed_message = MESSAGE_TEMPLATE.format(
        wallet=wallet, nonce=nonce_dict[wallet])

    message = encode_defunct(text=signed_message)
    print(signed_message, message, signature)

    recoveredAddress = w3.eth.account.recover_message(
        signable_message=message, signature=signature)
    print(signed_message, recoveredAddress, signature)

    encoded_jwt = jwt.encode({
        "wallet": wallet,
        "exp": datetime.datetime.today().timestamp() + 900000,
        "iat": datetime.datetime.today().timestamp()
    }, "secret", algorithm="HS256")
    return encoded_jwt, 200


@authenticate.route('/request', methods=["POST"])
def requestAuthenticate():
    data = request.get_json()
    wallet = Web3.toChecksumAddress(data["wallet"])
    # collection_id = request.args.get('signature')
    # collection_id = request.args.get('nonce')
    if wallet not in current_app.config["ADMIN_WALLETS"]:
        return {
            "message": "",
            "user": True
        }
# ['0x811a7c9334966401C22B79a55B6aCE749004D543']
# 0x811a7c9334966401c22b79a55b6ace749004d543
    nonce = uuid.uuid4().hex
    nonce_dict[Web3.toChecksumAddress(wallet)] = nonce
    # 'b46290528cd949498ce4cc86ca854173'

    return {
        "message": MESSAGE_TEMPLATE.format(wallet=wallet, nonce=nonce),
        "user": False
    }
