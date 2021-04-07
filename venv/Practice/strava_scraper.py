"""
Strava Scraper
selenium을 이용하여 구글 로그인을 한 후
내 Strava 운동 기록 정보에서 원하는 정보를 Scraping 해오기
"""

import os.path
from selenium import webdriver
from time import sleep
import pyautogui as pg
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import  WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


class Scraper:
    """Scraping 클래스"""

    # 절대 경로로 가져오기
    PATH = os.path.abspath("../chromedriver")
    LOGIN_URL = 'http://www.strava.com/login'
    ID = 'kthtim0704@gmail.com'
    PASSWORD = ''
    
    def __init__(self):
        # 크롬 웹드라이버 설정
        self.driver = webdriver.Chrome(self.PATH)

        # 페이지 로딩이 완료되기까지 몇 초 기다릴지 정하기
        self.driver.implicitly_wait(3)

        # 크롬을 통해 스트라바 접속
        self.driver.get(self.LOGIN_URL)

        self.PASSWORD = pg.password(text='ID : {} 의 비밀번호 입력'
                                    .format(self.ID), title='스트라바 스크레퍼')

    def google_login(self):
        """구글로 로그인"""
        self.driver.find_element_by_css_selector('#login_form > div.google > a').click()
        sleep(0.5)

        # 로그인 아이디 입력
        self.driver.find_element_by_css_selector('#identifierId').send_keys(self.ID)

        # 다음 버튼 클릭
        self.driver.find_element_by_css_selector('#identifierNext > div > button > div.VfPpkd-RLmnJb').click()
        sleep(0.5)
        
        # 비밀번호 입력
        self.driver.find_element_by_css_selector('#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input').send_keys(self.PASSWORD)

        # 다음 버튼 클릭
        self.driver.find_element_by_css_selector('#passwordNext > div > button > div.VfPpkd-RLmnJb').click()

        # 2단계 인증시 처리
        # 다시 요청 취소
        self.driver.find_element_by_css_selector('#toggle-c3').click()

    def scraping_activities(self):
        """내 활동 스크래핑 하기"""

        # 로그인 상태 기다리기
        element = WebDriverWait(self.driver, 30).until(
            EC.url_to_be('https://www.strava.com/dashboard#')
        )

        # 내 활동으로 이동
        self.driver.get('https://www.strava.com/athlete/training')
        sleep(0.5)

        # 비공개 체크
        self.driver.find_element_by_css_selector('#search-filters > label:nth-child(2)').click()

        # 내 활동들 모두 접근해서 정보 가져오기
        elements = self.driver.find_elements_by_css_selector('#search-results > tbody > tr:nth-child(1) > td.view-col.col-title > a')

        for element in elements:
            # 새 탭에서 열기
            element.send_keys(Keys.CONTROL + '\n')

        next_element = self.driver.find_element_by_css_selector('body > div.page.container > nav > div > ul > li:nth-child(2) > button')
        print(next_element.get_attribute('class'))


if __name__ == '__main__':
    scraper = Scraper()

    scraper.google_login()

    scraper.scraping_activities()
