import time
import json
import requests
from web3 import Web3, HTTPProvider, WebsocketProvider
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import Lock

CONTRACT_ADDRESS = "0xF2Ccf89d5C92036A8075F6da96E1bb970969AA47"
with open("abi.json", "r") as f:
    ape_abi = json.loads(f.read())
rpc_ws = "https://rinkeby.infura.io/v3/d5fccf7b8e244c3dbdaa6f68aff92f48"  # Node
web3 = Web3(HTTPProvider(rpc_ws))
contract = web3.eth.contract(
    address=web3.toChecksumAddress(CONTRACT_ADDRESS), abi=ape_abi
)

total_supply = contract.functions.totalSupply().call()


def snapshot(token_id):
    print(token_id)
    time.sleep(1)
    try:
        result = contract.functions.ownerOf(token_id).call()
        # lock.acquire()
        with open("./snapshotv2_execute/snapshot_NVC.txt", "a") as f:
            f.write(f"{token_id}|{result}\n")
        # lock.release()
    except Exception as error:
        # err_lock.acquire()
        with open("snapshotv2_execute/snapshot_error.txt", "a") as f:
            f.write(f"{token_id}|{str(error)}\n")
        # err_lock.release()


lock = Lock()
err_lock = Lock()
token_ids = [_ for _ in range(0, total_supply + 5)]
pool = ThreadPool(10)
pool.map(snapshot, token_ids)
