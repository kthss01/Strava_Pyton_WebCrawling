"""
파이썬 dictionary 연습
파일 입출력하기
dictionary 합치기
"""

# 딕셔너리 합치기 3.4 버전 이상
x = {'a': 1, 'b': 2}
y = {'b': 10, 'c': 11}
z = {'d': 9, 'z': 14, 'y': 13}

merged = {**x, **y, **z}  # 키값 중복되면 뒤에거에 덮어씌워짐

print(merged)

# update 메서드 이용하는 방법도 있음

# Dictionary 데이터를 파일로 저장하기
import pickle

# save data
with open('user.pickle', 'wb') as fw:
    pickle.dump(merged, fw)

# load data
with open('user.pickle', 'rb') as fr:
    load_data = pickle.load(fr)

# show data
print(load_data)

"""
참고로 json도 해보자
"""
import json

# save
with open('data.json', 'w') as json_file:
    json.dump(merged, json_file)  # 딕서녀리 자체를 json으로 저장 가능
    # json.dump(x, json_file)  # 이런 방법으로는 json 만들 수 없음
    # json.dump(y, json_file)
    # json.dump(z, json_file)

## 참고로 s 붙이면 포맷 데이터를 메모리에 만드는거 json.dumps
st_json = json.dumps(merged, indent=4)  # indent 들여쓰기
print(st_json)

# load
with open("data.json", "r") as st_json:
    st_python = json.load(st_json)

print(st_python)

"""
json에서 dictionary로 변환하는 방법
"""
json_data = '{ "p1": { "name": "chulsu", "age": 20 }, "p2": { "name": "younghee", "age": 22 } }'
dict_data = { "p1": { "name": "chulsu", "age": 20 }, "p2": { "name": "younghee", "age": 22 } }

# convert json to dict
result = json.loads(json_data)
print("parse_json result: %s" % type(result))
print(result)

# convert dict to json
result = json.dumps(dict_data)
print("convert_json result: %s" % type(result))
print(result)
