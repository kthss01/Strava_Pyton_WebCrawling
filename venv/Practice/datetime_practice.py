"""
datetime을 이용하여 날짜 비교하기
"""

import datetime

now = datetime.datetime.today()
print(now)
print("{}.{}.{} {}:{}".format(now.year, now.month, now.day, now.hour, now.minute))

t = "월화수목금토일"
week = t[now.weekday()]
print(f"{week}요일")

one_day = datetime.datetime(year=2018, month=3, day=18, hour=18, minute=30, microsecond=0)
that_day = datetime.datetime(year=2018, month=3, day=18, hour=13, minute=30, microsecond=0)

print(f"어느날 = {one_day}")
print(f"그날 = {that_day}")

check = ""
if one_day > that_day:
    check = "이후"
else:
    check = "이전"

print("어느날은 그날보다 {}이다.".format(check))