import datetime

reset_day = "2022-08-01"
delta = datetime.datetime.strptime(reset_day, "%Y-%m-%d") - datetime.datetime.today()
print(delta.days)
