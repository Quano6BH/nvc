from database_fetch import SqlConnector
import database_script as db
import datetime
import json


# Chạy update database mỗi ngày

# Ngày chạy update database
day = "2022-07-10"  # có thể dùng datetime.date.today() format theo dạng %Y-%m-%d
last_day = "2022-07-09"  # Ngày trước ngày chạy update database, dùng để fetch report và cập nhật số ngày holding + interest

collection_id = 1  # Mặc định collection_id là 1 vì hiện tại mới làm 1 collection

# Extract token_holders để sử dụng cho các function sau:
token_holders = db.extract_token_holders(f"1_{day}.txt")

wallets = [token_holder["wallet"] for token_holder in token_holders]

# Execute script INSERT INTO NVC.Wallet
sql = SqlConnector()
sql.execute_script(db.insert_wallets(wallets))

# Fetch Principal, Interest, UpdateAppliedId theo Update mới nhất:
sql = SqlConnector()
(_, principal, interest, update_applied_id) = sql.fetch_closest_update(
    day, collection_id
)

# Execute script INSERT INTO NVC.NftHolder
sql = SqlConnector()
sql.execute_script(
    db.insert_nft_holder(token_holders, collection_id, principal, interest, day)
)

# Fetch Report ngày trước đó (ngày hôm qua)
sql = SqlConnector()
report_day_1 = sql.fetch_report(last_day, collection_id)

# Generate Report mới nhất
# Launch day chỉ cần token_holder, existing_data = None, begin_month = True
# Các ngày tiếp theo existing_data = report ngày cũ, begin_month = False (begin_month = True tại ResetDate)
report = db.generate_report(
    token_holders, principal * interest / 100, report_day_1, False
)

# Execute script INSERT INTO NVC.HolderByDate
sql = SqlConnector()
sql.execute_script(
    db.insert_holder_by_date(report, collection_id, day, update_applied_id)
)
