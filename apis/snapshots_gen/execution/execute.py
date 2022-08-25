from config import Config
from sql_connector import CollectionDataLayer
import database_script

db_config = Config().DATABASE


def insert_wallets(wallets):
    CollectionDataLayer(db_config).insert_wallets(wallets)


def fetch_closest_update(date, collection_id):
    result = CollectionDataLayer(db_config).fetch_closest_update(date, collection_id)
    return (result[0][0], result[0][1], result[0][2], result[0][3])


def insert_nft_holder(token_holders, collection_id, principal, interest, snapshot_date):
    CollectionDataLayer(db_config).insert_nft_holder(
        token_holders, collection_id, principal, interest, snapshot_date
    )


def insert_nft_id(collection_id, collection_total_supply):
    CollectionDataLayer(db_config).insert_nft_id(collection_id, collection_total_supply)


def fetch_report_by_date(snapshot_date, collection_id):
    result = CollectionDataLayer(db_config).fetch_data_by_date(
        snapshot_date, collection_id
    )
    report_by_date = database_script.fetch_report_by_date(result)
    return report_by_date


def generate_new_report_by_date(token_holders, interest, last_day_report, begin_month):
    result = database_script.generate_new_report_by_date(
        token_holders, interest, last_day_report, begin_month
    )
    return result


def insert_holder_by_date(new_report, collection_id, snapshot_date, update_applied_id):
    CollectionDataLayer(db_config).insert_holder_by_date(
        new_report, collection_id, snapshot_date, update_applied_id
    )


def extract_token_holders(date, collection_id):
    result = database_script.extract_token_holders(date, collection_id)
    return result


def insert_holder_by_month(
    last_day_report, collection_id, reset_date, update_applied_id
):
    CollectionDataLayer(db_config).insert_holder_by_month(
        last_day_report, collection_id, reset_date, update_applied_id
    )
