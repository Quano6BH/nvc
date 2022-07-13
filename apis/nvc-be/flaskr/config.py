from web3 import Web3


class Config(object):
    DATABASE = {
        "host": "34.87.174.70",
        "port": 3306,
        "username": "root",
        "password": "Nvc123!@#",
        "database": "NVC"
    }
    FLASK_APP = "flaskr"
    ADMIN_WALLETS = [Web3.toChecksumAddress(address) for address in [
        "0x811a7c9334966401C22B79a55B6aCE749004D543",
        "0xF8eD875352236eF987a9c8855e9a6c0FE9B541db"
    ]]
