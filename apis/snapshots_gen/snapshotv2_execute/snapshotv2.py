import time
import json
import requests
from web3 import Web3, HTTPProvider
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import Lock

CONTRACT_ADDRESS = "0x8D5878530a76Dad92f425f784614925eD972765f"
with open("abi.json", "r") as f:
    ape_abi = json.loads(f.read())
rpc_ws = "https://young-little-brook.bsc-testnet.discover.quiknode.pro/"  # Node
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
        lock.acquire()
        with open("./snapshotv2_execute/snapshot_NVC.txt", "a") as f:
            f.write(f"{token_id}|{result}\n")
        lock.release()
    except Exception as error:
        err_lock.acquire()
        with open("snapshotv2_execute/snapshot_error.txt", "a") as f:
            f.write(f"{token_id}|{str(error)}\n")
        err_lock.release()


lock = Lock()
err_lock = Lock()
token_ids = [_ for _ in range(0, total_supply + 5)]
pool = ThreadPool(10)
pool.map(snapshot, token_ids)
