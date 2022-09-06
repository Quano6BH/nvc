
import datetime
from flask import request, Blueprint, current_app
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
    """Accept authenticate request
    ---
    parameters:
        - in: body
          description: The user to create.
          schema:
            type: object
            required:
              - userName
            properties:
              wallet:
                type: string
              signature:
                type: string
    responses:
      200:
        description: Request to authenticate
        examples:
          {
        "wallet": wallet,
        "exp": 2023-08-09,
        "iat": 2022-08-09
    }
    """
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
    """Request to authenticate
    ---
    parameters:
        - in: body
          description: The user to create.
          schema:
            type: object
            required:
              - userName
            properties:
              wallet:
                type: string
    responses:
      200:
        description: Request to authenticate
        examples:
          You are signing NVC Dashboard App using this nonce for address 0x66707b95dFCC2C17f37CeeE0037A17078431814A with 1
    """
    data = request.get_json()
    wallet = Web3.toChecksumAddress(data["wallet"])
    if wallet not in current_app.config["ADMIN_WALLETS"]:
        return {
            "message": "",
            "user": True
        }

    nonce = uuid.uuid4().hex
    nonce_dict[Web3.toChecksumAddress(wallet)] = nonce

    return {
        "message": MESSAGE_TEMPLATE.format(wallet=wallet, nonce=nonce),
        "user": False
    }
