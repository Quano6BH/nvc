import random
import json

from web3 import Web3, HTTPProvider


CONTRACT_ADDRESS = "0xDFd6E617711c89684d232799a74393b6f136DA7a"
with open("abi.json", "r") as f:
    ape_abi = json.loads(f.read())
rpc_ws = "https://young-little-brook.bsc-testnet.discover.quiknode.pro/"  # Node
web3 = Web3(HTTPProvider(rpc_ws))
contract = web3.eth.contract(
    address=web3.toChecksumAddress(CONTRACT_ADDRESS), abi=ape_abi
)

sender_address = web3.toChecksumAddress(
    "0xcd52C63Cee55CEA02A1B9350B0B9ccF1e0037713")
sender_pk = "034ce17442a77c04c8269c0f2e28ea8a6bb15378162167f7858ae0750b25cdd9"


lines = []
with open("new_wallet.txt", "r") as file:
    lines = file.readlines()

nonce = web3.eth.get_transaction_count(sender_address)
# for line in lines[90:100]:
#     split_line = line.split("|")
#     wallet_addresses = Web3.toChecksumAddress(split_line[0])
#     wallet_pk = split_line[1]

#     quantity = 20
#     print(wallet_addresses + "|" + wallet_pk)
#     print(nonce)
#     safe_mint_txn = contract.functions.setApprovalForAll(
#         wallet_addresses, quantity
#     ).buildTransaction(
#         {
#             "from": sender_address,
#             "gas": 300000,
#             "gasPrice": web3.eth.gas_price,
#             "nonce": nonce,
#         }
#     )

# nonce = nonce + 1
# signed_txn = web3.eth.account.sign_transaction(
#     safe_mint_txn, private_key=sender_pk)

# tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

# print(Web3.toHex(tx_token))
# web3.eth.waitForTransactionReceipt(Web3.toHex(tx_token), timeout=120)
for i in range(995, 996):
    split_line = lines[99].split("|")
    wallet_addresses = Web3.toChecksumAddress(split_line[0])
    wallet_pk = split_line[1]

    quantity = 20
    print(wallet_addresses + "|" + wallet_pk)
    print(nonce)
    safe_transfer_txn = contract.functions.safeTransferFrom(
        sender_address, web3.toChecksumAddress(
            '0xcd52C63Cee55CEA02A1B9350B0B9ccF1e0037713'), i
    ).buildTransaction(
        {
            "from": sender_address,
            "gas": 300000,
            "gasPrice": web3.eth.gas_price,
            "nonce": nonce,
        }
    )
    nonce = nonce + 1
    signed_txn = web3.eth.account.sign_transaction(
        safe_transfer_txn, private_key=sender_pk)

    tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

    print(Web3.toHex(tx_token))
    web3.eth.waitForTransactionReceipt(Web3.toHex(tx_token), timeout=120)
