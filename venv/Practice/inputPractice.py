# 파이썬 입력 방식 getpass
import getpass

# print('test')

# idle에서 작동 안하는거 같음
# 해결 방안 찾음 터미널을 출력 콘솔 내에서 실행하도록 설정
# word = getpass.getpass('Input Word: ')
# print(word)

# 다른 방법 - 직접 구현
import sys
import msvcrt

# lower() 소문자로 바꾸는 함수

password = ''
while True:
    x = ord(msvcrt.getch())
    if x == 13: # Enter
        break
    sys.stdout.write('*')
    password += chr(x)

print('\n' + password)



# pwd = input('pwd: ')
# print(pwd)