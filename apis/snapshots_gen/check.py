import database_script as db
from database_fetch import SqlConnector
import json

with open("final.json", "r") as file:
    data = json.loads(file.read())
for check in data:
    wallet = check["WalletId"]
    nft_id = int(check["NftId"])
    total_days = check["TotalDays"]
    interest = check["Interest"]
    sql = SqlConnector()
    (hold_day_in_month, interest_earned) = sql.check(wallet, nft_id)
    if hold_day_in_month == total_days:
        with open("check.txt", "a") as file:
            file.write(f"{data.index(check)}. dung roi\n")
    else:
        with open("check.txt", "a") as file:
            file.write(f"{data.index(check)}. o kia thang Nhan sai roi\n")
