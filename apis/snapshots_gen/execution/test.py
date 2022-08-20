import datetime
from turtle import up
import execute

# The ID of the collection:
collection_id = 1

month = 8

today = 21

collection_total_supply = 1000

# Ngày chạy update database
day_format = datetime.datetime(2022, month, today)
# có thể dùng datetime.date.today() format theo dạng %Y-%m-%d
last_day_format = day_format - datetime.timedelta(days=1)
# Ngày trước ngày chạy update database, dùng để fetch report và cập nhật số ngày holding + interest
date = day_format.strftime("%Y-%m-%d")
last_day = last_day_format.strftime("%Y-%m-%d")


def insert_nft_id(collection_id, collection_total_supply):
    # Run once: Create database for Nft Table
    execute.insert_nft_id(collection_id, collection_total_supply)


def insert_holder_by_date(date, collection_id):
    # Extract token holders, return token id with corresponding holder.
    token_holders = execute.extract_token_holders(date, collection_id)

    # Extract wallets form token_holders, for inserting database into Wallets Table.
    wallets = [token_holder["wallet"] for token_holder in token_holders]
    execute.insert_wallets(wallets)

    # Extracting principal, interest, update_applied_id from closest CollectionUpdate data.
    (_, principal, interest, update_applied_id) = execute.fetch_closest_update(
        date, collection_id
    )

    # Insert into NftHolder.
    execute.insert_nft_holder(token_holders, collection_id, principal, interest, date)

    # Generate last_day_report from database, to create new day report.
    last_day_report = execute.fetch_report_by_date(last_day, collection_id)

    # Generate new day report.
    today_report = execute.generate_new_report_by_date(
        token_holders,
        principal * interest / 100 / 365,
        last_day_report,
        False,
    )

    # Insert report into database, HolderByDate Table.
    execute.insert_holder_by_date(today_report, collection_id, date, update_applied_id)


def insert_holder_by_month():
    # Do this once every month after reset_date

    # Generate last_day_report from database, to create new day report.
    last_day_report = execute.fetch_report_by_date(last_day, collection_id)

    # Extracting principal, interest, update_applied_id from closest CollectionUpdate data.
    (_, _, _, update_applied_id) = execute.fetch_closest_update(date, collection_id)

    execute.insert_holder_by_month(
        last_day_report, collection_id, date, update_applied_id
    )
