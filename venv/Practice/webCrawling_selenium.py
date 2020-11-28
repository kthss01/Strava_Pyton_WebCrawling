# 절대경로 가져오기
import os.path
path = os.path.abspath("../chromedriver")
# print(path)

# 자동화 테스트를 위해 셀레니움(Selenium) 불러오기
from selenium import webdriver
from time import sleep

# 크롬 웹드라이버 경로 설정
driver = webdriver.Chrome(path)

# 크롬을 통해 구글 로그인 화면에 접속
loginUrl = 'https://www.strava.com/login'
driver.get(loginUrl)

sleep(0.5)
driver.find_element_by_xpath('//*[@id="login_form"]/div[2]/a').click()

# 로그인 아이디 입력
sleep(0.5)
id = 'kthtim0704@gmail.com'
driver.find_element_by_name('identifier').send_keys(id)

sleep(0.5)
driver.find_element_by_xpath('//*[@id="identifierNext"]/div/button/div[2]').click()

# 비밀번호 입력 받기
import sys
import msvcrt

password = ''
while True:
    x = ord(msvcrt.getch())
    if x == 13: # Enter 개행 문자
        break
    sys.stdout.write('*')
    password += chr(x)

print(password)
sleep(0.5)
driver.find_element_by_name('password').send_keys(id)
