import datetime
import random

# print("1.", datetime.date.today())
# print("2.", datetime.datetime.now())
# print("3.", datetime.time(6, 50, 0))
# # print(type(datetime.time(6, 50, 0)))
# print("4.", datetime.datetime(2023, 8, 6, 8, 17, 0))
# # print(type(datetime.datetime(2023, 8, 6, 8, 17, 0)))
# print("5.", datetime.date(2023, 8, 8))
# # print(type(datetime.date(2023, 8, 8)))
# current_time = datetime.datetime.now()
# print("6.", current_time.strftime('%m-%d-%Y %H-%M-%S'))


birthdate = datetime.date(2022, 12, 31)
today = datetime.date(2023, 1, 25)
day_diff = (today - birthdate).days
print(f"7. Day difference {day_diff}.")
print("8.", datetime.timedelta(days=10))

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$



# Calculate project completion date
start_date = datetime.date(2023, 9, 1)
task_duration = datetime.timedelta(days=30)
completion_date = start_date + task_duration

print(f"Task starts on: {start_date}")
print(f"Task duration: {task_duration.days} days")
print(f"Project completion date: {completion_date}")


# date_list = [datetime.date(2023, i, j ) for i in range(1, 12) for j in range(1,29)]
# random.shuffle(date_list)
# selected_list = date_list[:num_dates]