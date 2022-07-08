import database_script as db
from database_fetch import SqlConnector
import datetime

# # Ngày chạy update database
# day = datetime.datetime(2022, 7, 10)
# # có thể dùng datetime.date.today() format theo dạng %Y-%m-%d
# last_day = day - datetime.timedelta(days=1)
# # Ngày trước ngày chạy update database, dùng để fetch report và cập nhật số ngày holding + interest
# day = day.strftime("%Y-%m-%d")
# last_day = last_day.strftime("%Y-%m-%d")

collection_id = 1

# sql = SqlConnector()
# (_, principal, interest, update_applied_id) = sql.fetch_closest_update(
#     day, collection_id
# )
# sql = SqlConnector()
# report_last_day = sql.fetch_report(last_day, collection_id)
# sql = SqlConnector()
# sql.execute_script(
#     db.insert_holder_by_month(report_last_day, collection_id, day, update_applied_id)
# )

sql = SqlConnector()
sql.execute_script(db.insert_nft(collection_id))
