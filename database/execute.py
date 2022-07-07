from database_fetch import SqlConnector
import database_script as db
import datetime
import json

day = "2022-07-10"
last_day = "2022-07-09"
collection_id = 1

token_holders = db.extract_token_holders(f"1_{day}.txt")

wallets = [token_holder["wallet"] for token_holder in token_holders]

sql = SqlConnector()
sql.execute_script(db.insert_wallets(wallets))

sql = SqlConnector()
(_, principal, interest, update_applied_id) = sql.fetch_closest_update(
    day, collection_id
)
sql = SqlConnector()
sql.execute_script(
    db.insert_nft_holder(token_holders, collection_id, principal, interest, day)
)

sql = SqlConnector()
report_day_1 = sql.fetch_report(last_day, collection_id)


report = db.generate_report(
    token_holders, principal * interest / 100, report_day_1, False
)

sql = SqlConnector()
sql.execute_script(
    db.insert_holder_by_date(report, collection_id, day, update_applied_id)
)
