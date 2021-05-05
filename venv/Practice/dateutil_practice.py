"""
문자열의 시간 포맷을 datetime으로 만들기
"""

from dateutil.parser import parse
import datetime
import time

date_str = "2021년 4월 16일(금요일) 오후 10:58"
# print(parse(date_str))  # 한글이라 안됨

# strftime 쓰는 것도 애매함

# 그냥 직접 구현 split으로

token = date_str.split(' ')

year = token[0][:-1]
# year = token[0][2:-1]  # 두 자리만 가져오기
month = token[1][:-1]
week = token[2][-4:-3]
day = token[2][:-6]
am_pm = token[3]
hour, minute = token[4].split(":")
if am_pm == '오후':
    hour = str(int(hour) + 12)

# print("{}.{}.{}({}) {}:{}".format(year, month, day, week, hour, minute))

dt = datetime.datetime(
        year=int(year), month=int(month), day=int(day),
        hour=int(hour), minute=int(minute))

# print(dt.isoformat())

w = '월화수목금토일'

print(dt.strftime('%y.%m.%d') + f'({w[dt.weekday()]}) {dt.hour}:{dt.minute}')

# time_str = "3:55:33"
# time_str2 = "5:23:33"
# # print(parse(time_str))
# # print(type(parse(time_str)))
# dt1 = parse(time_str)
# dt2 = parse(time_str2)
#
# print(dt2 - dt1)
# print(dt2 + datetime.timedelta(hours=dt1.hour, minutes=dt1.minute, seconds=dt1.second))

