from database_fetch import SqlConnector


def insert_wallets(wallets):
    script = "INSERT IGNORE INTO NVC.Wallet(Address) VALUES"
    for wallet in wallets:
        script += f"('{wallet}'),\n"
    script = script[: len(script) - 2] + ";"
    return script


def insert_nft(collection_id, total_supply=10000):
    script = f"INSERT INTO NVC.Nft(TokenId, CollectionId) VALUES"
    for i in range(0, total_supply):
        script += f"({i},{collection_id}),\n"
    script = script[: len(script) - 2] + ";"
    return script


def insert_nft_holder(token_holders, collection_id, principal, interest, snapshot_date):
    script = f"INSERT INTO NVC.NftHolder (TokenId, CollectionId, Holder, Principal, Interest, SnapshotDate) VALUES"
    for row in token_holders:
        token_id = row["token_id"]
        wallet = row["wallet"]
        script += f"({token_id},{collection_id},'{wallet}',{principal}, {interest}, '{snapshot_date}'),\n"
    script = script[0 : len(script) - 2] + ";"
    return script


def insert_holder_by_date(report, collection_id, snapshot_day, update_applied_id):
    script = "INSERT INTO NVC.HolderByDate (Holder, TokenId, CollectionId, HoldDays, HoldDaysInMonth, InterestEarned, InterestEarnedInMonth, SnapshotDate, UpdateAppliedId, Holding) VALUES"
    for holder in report.keys():
        for token_id in report[holder]["token_ids"].keys():
            hold_days = report[holder]["token_ids"][token_id]["holding_day"]
            hold_days_in_month = report[holder]["token_ids"][token_id][
                "holding_day_in_month"
            ]
            interest_earned = report[holder]["token_ids"][token_id]["interest"]
            interest_earned_in_month = report[holder]["token_ids"][token_id][
                "interest_in_month"
            ]
            holding = 1 if report[holder]["token_ids"][token_id]["holding"] else 0
            script += f"('{holder}',{token_id}, {collection_id},{hold_days}, {hold_days_in_month},{interest_earned}, {interest_earned_in_month},'{snapshot_day}',{update_applied_id}, {holding}),\n"
    script = script[: len(script) - 2] + ";"
    return script


def insert_holder_by_month(report, collection_id, reset_date, update_applied_id):
    script = "INSERT INTO NVC.HolderByMonth (Holder, CollectionId, ResetDate, TotalNFTs, InterestEarned, UpdateAppliedId) VALUES"
    for holder in report.keys():
        total_nfts = 0
        interest_earned = 0
        for token_id in report[holder]["token_ids"].keys():
            total_nfts += report[holder]["token_ids"][token_id]["holding_day"]
            interest_earned += report[holder]["token_ids"][token_id]["interest"]
        script += f"('{holder}',{collection_id},'{reset_date}',{total_nfts},{interest_earned},{update_applied_id}),\n"
    script = script[: len(script) - 2] + ";"
    return script


def extract_token_holders(file_name):
    with open(f"snapshot/{file_name}", "r") as file:
        lines = file.readlines()
    token_holders = []
    for line in lines:
        token_id = line.split("|")[0]
        wallet = line.split("|")[1].replace("\n", "")
        token_holders.append({"token_id": token_id, "wallet": wallet})
    return token_holders


def generate_report(
    adding_token_holders, interest, existing_data=None, begin_month=False
):

    data = existing_data.copy() if existing_data else {}

    for wallet in data:
        for token_id in data[wallet]["token_ids"]:
            data[wallet]["token_ids"][token_id]["holding"] = False

    for token_holder in adding_token_holders:
        token_id = token_holder["token_id"]
        holder = token_holder["wallet"]
        increment_holding_day = 1

        # chua co holder
        if not holder in data.keys():
            data[holder] = {
                "token_ids": {
                    token_id: {
                        "holding_day": increment_holding_day,
                        "holding_day_in_month": increment_holding_day,
                        "interest": interest,
                        "interest_in_month": interest,
                        "holding": True,
                    }
                }
            }

        # co holder
        else:
            if not existing_data:
                data[holder]["token_ids"][token_id] = {
                    "holding_day": increment_holding_day,
                    "holding_day_in_month": increment_holding_day,
                    "interest": interest,
                    "interest_in_month": interest,
                    "holding": True,
                }

            else:
                # co token
                if token_id in data[holder]["token_ids"]:
                    data[holder]["token_ids"][token_id]["holding_day"] += 1
                    data[holder]["token_ids"][token_id]["interest"] += interest
                    if begin_month:
                        data[holder]["token_ids"][token_id][
                            "holding_day_in_month"
                        ] = increment_holding_day
                        data[holder]["token_ids"][token_id][
                            "interest_in_month"
                        ] = interest

                    else:
                        data[holder]["token_ids"][token_id][
                            "holding_day_in_month"
                        ] += increment_holding_day
                        data[holder]["token_ids"][token_id][
                            "interest_in_month"
                        ] += interest

                    data[holder]["token_ids"][token_id]["holding"] = True
                # chua co token
                else:
                    data[holder]["token_ids"][token_id] = {
                        "holding_day": increment_holding_day,
                        "interest": interest,
                        "interest_in_month": interest,
                        "holding_day_in_month": increment_holding_day,
                        "holding": True,
                    }

    return data
