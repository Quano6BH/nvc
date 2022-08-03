
from database_fetch import SqlConnector
import json
update_script= f"""
SELECT Holder,TokenId,SnapshotDate,InterestEarnedInMonth, cu.Interest, cu.Principal
        FROM HolderByDate hbd 
                
            INNER JOIN CollectionUpdate cu 
                ON cu.Id = hbd.UpdateAppliedId  
            INNER JOIN Wallet w 
                ON hbd.Holder = w.Address  
        
        WHERE hbd.CollectionId = 1
        AND w.Kyc = b'1'
        AND Paid = b'0'
        -- AND TokenId = 0
        AND Holding = b'1'
        AND hbd.SnapshotDate <= '2022-05-25' 
        ORDER BY TokenId ASC, SnapshotDate ASC
"""


collection_id = 1
date_time = "2022-07-01"
sql = SqlConnector()
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
        AND hbd.SnapshotDate <= '{date_time}' 
        ORDER BY TokenId ASC, SnapshotDate ASC
"""
data = sql.fetch_by_script(script)

lines = []
with open("./data/montly/report.txt", "w") as f:
    for item in data:
        lines.append('|'.join([str(inner_item) for inner_item in item]))
    f.write("\n".join(lines))


def cal_interest(percent_interest_per_year, principal):
    return principal * (percent_interest_per_year/365) / 100


is_done_a_row = False
columns = data[0]
result = []

first = data[1]
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
    print(f"{current_holder},{currentRow['WalletId']},{current_token_id},{currentRow['NftId']},{str(condition)}")
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

a_lines=""

a_lines+=f"WalletId|NftId|Date1|Date2|TotalDays|Interest\n"
for item in result:
    
    a=    item["WalletId"] 
    b=    item["NftId"] 
    c=    item["Date1"] 
    d=    item["Date2"] 
    e=    item["TotalDays"] 
    f=    item["Interest"] 
    kk=f"{a}|{b}|{c}|{d}|{e}|{f}\n"
    print(kk)
    a_lines+=kk
with open("./data/montly/final.txt", "w") as f:
    f.write(a_lines)
