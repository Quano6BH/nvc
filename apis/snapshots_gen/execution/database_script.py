def extract_token_holders(date, collection_id):
    month = date.split("-")[1]
    year = date.split("-")[0]
    with open(
        f"./snapshot/{collection_id}/{year}-{month}/{collection_id}_{date}.txt", "r"
    ) as file:
        lines = file.readlines()
    token_holders = []
    for line in lines:
        token_id = line.split("|")[0]
        wallet = line.split("|")[1].replace("\n", "")
        token_holders.append({"token_id": token_id, "wallet": wallet})
    return token_holders


def fetch_report_by_date(data_by_date):
    data = {}
    for row in data_by_date:
        interest = float(row[4])
        interest_in_month = float(row[5])
        try:
            data[row[0]]["token_ids"][f"{row[1]}"] = {
                "holding_day": row[2],
                "holding_day_in_month": row[3],
                "interest": interest,
                "interest_in_month": interest_in_month,
            }
        except:
            data[row[0]] = {
                "token_ids": {
                    f"{row[1]}": {
                        "holding_day": row[2],
                        "holding_day_in_month": row[3],
                        "interest": interest,
                        "interest_in_month": interest_in_month,
                    }
                }
            }
            continue
    return data


def generate_new_report_by_date(
    adding_token_holders, interest, existing_data=None, begin_month=False
):

    data = existing_data.copy() if existing_data else {}

    for wallet in data:
        for token_id in data[wallet]["token_ids"]:
            data[wallet]["token_ids"][token_id]["holding"] = False
    if begin_month:
        for wallet in data:
            for token_id in data[wallet]["token_ids"]:
                data[wallet]["token_ids"][token_id]["holding"] = False
                data[wallet]["token_ids"][token_id]["holding_day_in_month"] = 0
                data[wallet]["token_ids"][token_id]["interest_in_month"] = 0

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
