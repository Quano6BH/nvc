import datetime
import execute
import schedule

# The ID of the collection:
collection_id = 1

collection_total_supply = 1000

reset_date = 26

# Ngày chạy update database
# date = datetime.datetime(2022, 8, 21)
date = datetime.datetime.today()


def get_previous_date(date: datetime):
    previous_date = date - datetime.timedelta(days=1)
    return previous_date


def to_ymd_format(date: datetime):
    return date.strftime("%Y-%m-%d")


def insert_nft_id(collection_id, collection_total_supply):
    """
    Run once: Create database for Nft Table
    """
    execute.insert_nft_id(collection_id, collection_total_supply)


def insert_holder_by_date(insert_date, collection_id):
    insert_date_str = to_ymd_format(insert_date)
    prev_date = get_previous_date(insert_date)
    prev_date_str = to_ymd_format(prev_date)

    # Extract token holders, return token id with corresponding holder.
    token_holders = execute.extract_token_holders(
        insert_date_str, collection_id)

    # Extract wallets form token_holders, for inserting database into Wallets Table.
    wallets = [token_holder["wallet"] for token_holder in token_holders]
    execute.insert_wallets(wallets)

    # Extracting principal, interest, update_applied_id from closest CollectionUpdate data.
    (reset_date, principal, interest, update_applied_id) = execute.fetch_closest_update(
        insert_date, collection_id
    )

    # Insert into NftHolder.
    execute.insert_nft_holder(
        token_holders, collection_id, principal, interest, insert_date_str
    )

    # Generate last_day_report from database, to create new day report.
    prev_day_report = execute.fetch_report_by_date(
        prev_date_str, collection_id)

    # Generate new day report.
    today_report = execute.generate_new_report_by_date(
        token_holders,
        principal * interest / 100 / 365,
        prev_day_report,
        True if insert_date_str == reset_date else False,
    )

    # Insert report into database, HolderByDate Table.
    execute.insert_holder_by_date(
        today_report, collection_id, insert_date_str, update_applied_id
    )


def insert_holder_by_month(insert_date, collection_id):
    """
    Do this once every month after reset_date
    """
    insert_date_str = to_ymd_format(insert_date)
    prev_date = get_previous_date(insert_date)
    prev_date_str = to_ymd_format(prev_date)
    # Generate last_day_report from database, to create new day report.
    last_day_report = execute.fetch_report_by_date(
        prev_date_str, collection_id)

    # Extracting principal, interest, update_applied_id from closest CollectionUpdate data.
    (_, _, _, update_applied_id) = execute.fetch_closest_update(
        insert_date_str, collection_id
    )

    execute.insert_holder_by_month(
        last_day_report, collection_id, insert_date, update_applied_id
    )


schedule.every().day.at("18:02").do(insert_holder_by_date,
                                    insert_date=date, collection_id=collection_id)

while True:
    schedule.run_pending()
