import time
import json
from web3 import Web3, HTTPProvider
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import Lock
import datetime
import requests

collection_id = 1
date = str(datetime.date.today())
year = date.split("-")[0]
month = date.split("-")[1]
day = date.split("-")[2]


snapshot_file = "./apis/snapshots_gen/snapshotv2_execute/snapshot_NVC.txt"
snapshot_file_error = "./apis/snapshots_gen/snapshotv2_execute/snapshot_error.txt"

with open("./apis/snapshots_gen/snapshotv2_execute/abi.json", "r") as f:
    ape_abi = json.loads(f.read())
rpc_ws = "https://zdjaypaos4ff.usemoralis.com:2053/server"  # Node
web3 = Web3(HTTPProvider(rpc_ws))


lock = Lock()
err_lock = Lock()


def get_total(collection_address):

    url = f"https://deep-index.moralis.io/api/v2/nft/{collection_address}?chain=bsc&format=decimal"

    headers = {
        "Accept": "application/json",
        "X-API-Key": "BcTVplgprvuYp6NYBWDDwT3PjKHo7jXnyO45wILPRmzuIXXgxm9ImVsLpot2Qnxm"
    }

    response = requests.get(url, headers=headers)

    # print(response.text)
    return json.loads(response.text)['total']


def get_owner(collection_address, token_id):

    url = f"https://deep-index.moralis.io/api/v2/nft/{collection_address}/{token_id}/owners?chain=bsc&format=decimal"

    headers = {
        "Accept": "application/json",
        "X-API-Key": "BcTVplgprvuYp6NYBWDDwT3PjKHo7jXnyO45wILPRmzuIXXgxm9ImVsLpot2Qnxm"
    }

    response = requests.get(url, headers=headers)
    print(response.text)
    print(json.loads(response.text)['result'][0]['owner_of'])
    return json.loads(response.text)['result'][0]['owner_of']


def get_contract(collection_address):
    contract = web3.eth.contract(
        address=web3.toChecksumAddress(collection_address), abi=ape_abi
    )
    return contract


def snapshot(data_tuple):
    (token_id, collection_address) = data_tuple
    contract = get_contract(collection_address)
    print(token_id)
    time.sleep(5)
    try:
        # result = contract.functions.ownerOf(token_id).call()
        result = get_owner(collection_address, token_id)
        time.sleep(5)
        lock.acquire()
        with open(snapshot_file, "a") as f:
            f.write(f"{token_id}|{result}\n")
        lock.release()
    except Exception as error:
        err_lock.acquire()
        with open("snapshotv2_execute/snapshot_error.txt", "a") as f:
            f.write(f"{token_id}|{str(error)}\n")
        err_lock.release()


def sort():
    with open(snapshot_file, "r") as file:
        lines = file.readlines()
    lines.sort(key=lambda line: int(line.split("|")[0]))
    with open(snapshot_file, "w") as file:
        file.writelines(lines)


def count_error(total_supply):
    with open(snapshot_file, "r") as file:
        lines = file.readlines()
    token_ids = [int(x.split("|")[0]) for x in lines]
    missing_token_ids = []
    for token_id in range(0, total_supply):
        if token_id not in token_ids:
            missing_token_ids.append(token_id)
    return missing_token_ids


def on_retry_failed():
    print("fail too much")
    pass


def runner(collection_address):
    contract = get_contract(collection_address)
    # total_supply = contract.functions.totalSupply().call()
    total_supply = get_total(collection_address)

    with open(snapshot_file, "w") as f:
        f.write("")
    with open(snapshot_file_error, "w") as f:
        f.write("")

    datas = [(id, collection_address)for id in range(0, total_supply)]
    pool = ThreadPool(1)
    pool.map(snapshot, datas)
    sort()
    missing_token_ids = count_error(total_supply)
    if len(missing_token_ids) > 0:
        pool = ThreadPool(10)
        pool.map(snapshot, missing_token_ids, collection_address)
        sort()
        missing_token_ids = count_error(total_supply)
        if len(missing_token_ids) > 0:
            on_retry_failed()
    with open(snapshot_file, "r") as f:
        success_snapshots = f.read()
    with open(f"./apis/snapshots_gen/snapshot/{collection_id}/{year}-{month}/{collection_id}_{year}-{month}-{day}.txt", "w")as file:
        file.write(success_snapshots)
