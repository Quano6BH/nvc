from database_fetch import SqlConnector
import database_script as db
import datetime


for i in range(1, 12):
    # Chạy update database mỗi ngày

    # Ngày chạy update database
    day = datetime.datetime(2022, 7, i)
    # có thể dùng datetime.date.today() format theo dạng %Y-%m-%d
    last_day = day - datetime.timedelta(days=1)
    # Ngày trước ngày chạy update database, dùng để fetch report và cập nhật số ngày holding + interest
    day = day.strftime("%Y-%m-%d")
    last_day = last_day.strftime("%Y-%m-%d")
    collection_id = 2  # Mặc định collection_id là 1 vì hiện tại mới làm 1 collection

    # Extract token_holders để sử dụng cho các function sau:
    token_holders = db.extract_token_holders(day, collection_id)

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
    report_last_day = sql.fetch_report(last_day, collection_id)

    # Generate Report mới nhất
    # Launch day chỉ cần token_holder, existing_data = None, begin_month = True
    # Các ngày tiếp theo existing_data = report ngày cũ, begin_month = False (begin_month = True tại ResetDate)
    report = db.generate_report(
        token_holders,
        principal * interest / 100 / 365,
        report_last_day,
        True if i == 1 else False,
    )

    # Execute script INSERT INTO NVC.HolderByDate
    sql = SqlConnector()
    sql.execute_script(
        db.insert_holder_by_date(report, collection_id, day, update_applied_id)
    )
