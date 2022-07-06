import json
from database_fetch import SqlConnector
import datetime


def insert_wallets(wallets):
    script = "INSERT IGNORE INTO NVC.Wallet(Address) VALUES"
    for wallet in wallets:
        script += f"('{wallet}'),\n"
    script = script[: len(script) - 2] + ";"
    with open("wallet.txt", "w") as file:
        file.write(script)


def insert_nft(collection_id, total_supply=10000):
    script = f"INSERT INTO NVC.Nft(TokenId, CollectionId) VALUES"
    for i in range(0, total_supply):
        script += f"({i},{collection_id}),\n"
    script = script[: len(script) - 2] + ";"
    with open("nft.txt", "w") as file:
        file.write(script)


def insert_nft_holder(token_holders, collection_id, principal, interest, snapshot_date):
    script = ""
    for row in token_holders:
        token_id = row["token_id"]
        wallet = row["wallet"]
        script += f"({token_id},{collection_id},'{wallet}',{principal}, {interest}, '{snapshot_date}'),\n"
    script = script[0 : len(script) - 2] + ";"
    with open("nft_holder.txt", "w") as file:
        file.write(script)


def insert_holder_by_date(data, collection_id, snapshot_day, update_applied_id):
    script = "INSERT INTO NVC.HolderByDate (Holder, TokenId, CollectionId, HoldDays, InterestEarned, SnapshotDate, UpdateAppliedId) VALUES"
    for holder in data.keys():
        for token_id in data[holder]["token_ids"].keys():
            hold_days = data[holder]["token_ids"][token_id]["holding_day"]
            interest_earned = data[holder]["token_ids"][token_id]["interest"]
            script += f"('{holder}',{token_id}, {collection_id},{hold_days},{interest_earned},'{snapshot_day}',{update_applied_id}),\n"
    script = script[: len(script) - 2] + ";"
    with open("holder_by_date.txt", "w") as file:
        file.write(script)


def extract_token_holders(file_name):
    with open(f"snapshot/{file_name}", "r") as file:
        lines = file.readlines()
    token_holders = []
    for line in lines:
        token_id = line.split("|")[0]
        wallet = line.split("|")[1].replace("\n", "")
        token_holders.append({"token_id": token_id, "wallet": wallet})
    return token_holders


def generate_report(adding_token_holders, interest, existing_data=None):

    data = existing_data or {}
    for token_holder in adding_token_holders:
        token_id = token_holder["token_id"]
        holder = token_holder["wallet"]
        increment_holding_day = 1
        if not holder in data.keys():
            data[holder] = {
                "token_ids": {
                    token_id: {
                        "holding_day": increment_holding_day,
                        "interest": interest,
                    }
                }
            }
        else:
            if not existing_data:
                data[holder]["token_ids"][token_id] = {
                    "holding_day": increment_holding_day,
                    "interest": interest,
                }

            else:
                if token_id in data[holder]["token_ids"]:
                    data[holder]["token_ids"][token_id]["holding_day"] += 1
                    data[holder]["token_ids"][token_id]["interest"] += interest
                else:
                    data[holder]["token_ids"][token_id] = {
                        "holding_day": increment_holding_day,
                        "interest": interest,
                    }

    return data


# token_holders = extract_data("")
# wallets = [token_holder["wallet"] for token_holder in token_holders]

# insert_nft_holder(
#     token_holders,
#     collection_id=1,
#     principal=principal,
#     interest=interest,
#     snapshot_date=snapshot_date,
# )
# insert_holder_by_date("2022-07-01.json")
SQL = SqlConnector()
collection_id = 1
snapshot_date = datetime.date.today()
_, principal, interest, update_applied_id = SQL.fetch_closest_update(
    snapshot_date, collection_id
)
print(principal)
print(interest)
# token_holders = extract_token_holders("1_2022-07-01.txt")
# report = generate_report(token_holders, 1000 * (1.5 / 100), existing_data=None)
# insert_holder_by_date(report, collection_id, snapshot_date, 1)
