import datetime
import execution.execute as ex
import schedule
import snapshotv2_execute.snapshotv2 as snapshot

# The ID of the collection:
collection_id = 2

collection_total_supply = 560

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
    ex.insert_nft_id(collection_id, collection_total_supply)


def insert_holder_by_date(insert_date, collection_id):
    insert_date_str = to_ymd_format(insert_date)
    prev_date = get_previous_date(insert_date)
    prev_date_str = to_ymd_format(prev_date)

    # Extract token holders, return token id with corresponding holder.
    token_holders = ex.extract_token_holders(
        insert_date_str, collection_id)

    # Extract wallets form token_holders, for inserting database into Wallets Table.
    wallets = [token_holder["wallet"] for token_holder in token_holders]
    ex.insert_wallets(wallets)

    # Extracting principal, interest, update_applied_id from closest CollectionUpdate data.
    (reset_date, principal, interest, update_applied_id) = ex.fetch_closest_update(
        insert_date, collection_id
    )

    # Insert into NftHolder.
    ex.insert_nft_holder(
        token_holders, collection_id, principal, interest, insert_date_str
    )

    # Generate last_day_report from database, to create new day report.
    prev_day_report = ex.fetch_report_by_date(
        prev_date_str, collection_id)

    # Generate new day report.
    today_report = ex.generate_new_report_by_date(
        token_holders,
        principal * interest / 100 / 365,
        prev_day_report,
        True if insert_date_str == reset_date else False,
    )

    # Insert report into database, HolderByDate Table.
    ex.insert_holder_by_date(
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
    last_day_report = ex.fetch_report_by_date(
        prev_date_str, collection_id)

    # Extracting principal, interest, update_applied_id from closest CollectionUpdate data.
    (_, _, _, update_applied_id) = ex.fetch_closest_update(
        insert_date_str, collection_id
    )

    ex.insert_holder_by_month(
        last_day_report, collection_id, insert_date, update_applied_id
    )


def get_collection_address(collection_id):
    collection_address = ex.fetch_collection_address(collection_id)
    print(collection_address[0][0])
    return collection_address[0][0]


def runner(collection_id):
    date = datetime.datetime.today()
    collection_address = get_collection_address(collection_id)
    snapshot.runner(collection_id, collection_address)
    insert_holder_by_date(date, collection_id)
    print("complete")


schedule.every().day.at("10:48").do(runner,
                                    collection_id=collection_id)

while True:
    schedule.run_pending()

# insert_nft_id(collection_id, collection_total_supply)
