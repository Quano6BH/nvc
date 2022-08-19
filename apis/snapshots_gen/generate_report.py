from database_fetch import SqlConnector
import json


def update_paid(from_date, to_date, collection_id):
    update_script = f"""
    UPDATE HolderByDate hbd
                INNER JOIN Wallet w
                    ON hbd.Holder = w.Address
            SET Paid = b'1'

            WHERE hbd.CollectionId = {collection_id}
            AND w.Kyc = b'1'
            AND Paid = b'0'
            -- AND TokenId = 0
            AND Holding = b'1'
            {f"AND hbd.SnapshotDate >= '{from_date}'" if from_date else "" }
            AND hbd.SnapshotDate <= '{to_date}'
    """

    sql = SqlConnector()
    sql.execute_script(update_script)
    update_script = f"""
    UPDATE HolderByDate hbd
                INNER JOIN Wallet w
                    ON hbd.Holder = w.Address
            SET Paid = b'1'

            WHERE hbd.CollectionId = {collection_id}
            AND w.Kyc = b'1'
            AND Paid = b'0'
            -- AND TokenId = 0
            AND Holding = b'1'
            {f"AND hbd.SnapshotDate >= '{from_date}'" if from_date else "" }
            AND hbd.SnapshotDate <= '{to_date}'
    """

    sql = SqlConnector()
    sql.execute_script(update_script)


def fetch_interest_date(from_date, to_date, collection_id, to_file):

    script = f"""
    SELECT Holder,TokenId,SnapshotDate,InterestEarnedInMonth, cu.Interest, cu.Principal
        FROM HolderByDate hbd

            INNER JOIN CollectionUpdate cu
                ON cu.Id = hbd.UpdateAppliedId
            INNER JOIN Wallet w
                ON hbd.Holder = w.Address

        WHERE hbd.CollectionId = {collection_id}
        AND w.Kyc = b'1'
        AND Paid = b'0'
        -- AND TokenId = 0
        AND Holding = b'1'
        {f"AND hbd.SnapshotDate >= '{from_date}'" if from_date else "" }
        AND hbd.SnapshotDate <= '{to_date}'
        ORDER BY TokenId ASC, SnapshotDate ASC
    """

    sql = SqlConnector()
    data = sql.fetch_by_script(script)

    lines = []
    with open(to_file, "w") as f:
        for item in data:
            lines.append('|'.join([str(inner_item) for inner_item in item]))
        f.write("\n".join(lines))
    return data


def cal_interest(percent_interest_per_year, principal):
    return principal * (percent_interest_per_year/365) / 100


def to_csv_file(data):
    columns = data[0]
    result = []
    first = data[1]
    # print('No Data')
    # exit()
    currentRow = {
        "WalletId": first[columns.index("Holder")],
        "NftId": first[columns.index("TokenId")],
        "Date1": str(first[columns.index("SnapshotDate")]),
        "Date2": str(first[columns.index("SnapshotDate")]),
        "TotalDays": 1,
        "Interest": cal_interest(first[columns.index("Interest")], first[columns.index("Principal")]),
    }
    for row in data[2:]:
        current_holder = row[columns.index("Holder")]
        current_token_id = row[columns.index("TokenId")]
        current_interest = row[columns.index("Interest")]
        current_date = str(row[columns.index("SnapshotDate")])
        current_principal = row[columns.index("Principal")]
        condition = current_holder != currentRow["WalletId"] or current_token_id != currentRow["NftId"]
        # print(
        #     f"{current_holder},{currentRow['WalletId']},{current_token_id},{currentRow['NftId']},{str(condition)}")
        if(condition):
            result.append(currentRow)
            currentRow = {}
            currentRow["WalletId"] = current_holder
            currentRow["NftId"] = current_token_id
            currentRow["Date1"] = current_date
            currentRow["Date2"] = current_date
            currentRow["TotalDays"] = 1
            currentRow["Interest"] = cal_interest(
                current_interest, current_principal)
        else:
            currentRow["Date2"] = current_date
            currentRow["TotalDays"] += 1
            currentRow["Interest"] += cal_interest(
                current_interest, current_principal)
    return result


collection_id = 2
from_date = "2022-04-26"
to_date = "2022-07-25"

data = fetch_interest_date(
    from_date=from_date,
    to_date=to_date, collection_id=collection_id, to_file="./data/monthly/report.txt")
print(len(data))
result = to_csv_file(data=data)
a_lines = ""
delimiter = ","
a_lines += f"WalletId{delimiter}NftId{delimiter}Date1{delimiter}Date2{delimiter}TotalDays{delimiter}Interest\n"
for item in result:

    a = item["WalletId"]
    b = item["NftId"]
    c = item["Date1"]
    d = item["Date2"]
    e = item["TotalDays"]
    f = item["Interest"]
    kk = f"{a}{delimiter}{b}{delimiter}{c}{delimiter}{d}{delimiter}{e}{delimiter}{f}\n"
    # print(kk)
    a_lines += kk
with open(f"./data/monthly/to {to_date}.csv", "w") as f:
    f.write(a_lines)
# update_paid(from_date=from_date, to_date=to_date, collection_id=collection_id)
