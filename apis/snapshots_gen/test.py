import database_script as db
from database_fetch import SqlConnector
import datetime

# Insert NVC.Nft
sql = SqlConnector()
sql.execute_script(db.insert_nft(1, 560))
print("done")
input()

# month = 8
# collection_id = 2


# # Ngày chạy update database
# day = datetime.datetime(2022, month, 25)
# # có thể dùng datetime.date.today() format theo dạng %Y-%m-%d
# last_day = day
# # last_day = day - datetime.timedelta(days=1)
# # Ngày trước ngày chạy update database, dùng để fetch report và cập nhật số ngày holding + interest
# day = day.strftime("%Y-%m-%d")
# last_day = last_day.strftime("%Y-%m-%d")


# sql = SqlConnector()
# (_, principal, interest, update_applied_id) = sql.fetch_closest_update(
#     day, collection_id
# )
# sql = SqlConnector()
# report_last_day = sql.fetch_report(last_day, collection_id)
# sql = SqlConnector()
# aaa = db.insert_holder_by_month(
#     report_last_day, collection_id, day, update_applied_id)
# print(aaa)
# sql.execute_script(aaa)
