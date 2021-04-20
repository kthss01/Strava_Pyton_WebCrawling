"""
subprocess
현재 소스코드 안에서 다른 프로세스를 실행하게 해주며
그 과정에서 데이터의 입출력을 제어할 수 있음
"""

# -*- coding: utf-8 -*-

import subprocess

# subprocess.run(['dir'], shell=True, check=True)
# subprocess.call(['dir'], shell=True)
# subprocess.call(['test.py'], shell=True)  # 이상하게 안됨 run -> call로 바뀐듯
import sys

# subprocess.run(args=[sys.executable, 'test.py'])

p1 = subprocess.run(args=["dir"], shell=True, capture_output=True)
# print(p1.stdout.decode())
print(p1.stdout.decode('cp949'))
# print(p1.stdout.decode('euc-kr'))

# f = open('output.txt', 'w')
# out = subprocess.check_output(args=[sys.executable, 'test.py'], shell=True, encoding='cp949')
# f.write(out)
# f.close()
