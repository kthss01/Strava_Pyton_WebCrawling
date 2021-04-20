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


class Activity:
    """Activity 클래스 (활동 클래스)"""

    def __init__(self, sport, date, location, title, description, distance,
                 moving_time, altitude, calory, total_time):
        self.user = "태훈 김"

        self.sport = sport
        self.date = date
        self.location = location
        self.title = title
        self.description = description
        self.distance = distance
        self.moving_time = moving_time
        self.altitude = altitude
        self.calory = calory
        self.total_time = total_time

    def __str__(self):
        return f"스포츠: {self.sport}, 제목: {self.title}, 날짜: {self.date}, 위치: {self.location}\n" + \
               f"내용: {self.description}, 이동 시간: {self.moving_time}, 고도: {self.altitude}\n" + \
               f"칼로리: {self.calory}, 경과 시간: {self.total_time}\n"


class Riding(Activity):
    """Riding Activity 클래스 (활동 클래스 중 라이딩 클래스)"""

    def __init__(self, sport, date, location, title, description, distance,
                 moving_time, altitude, calory, total_time,
                 power, energy, avg_speed, max_speed):

        super().__init__(sport, date, location, title, description, distance,
                 moving_time, altitude, calory, total_time)

        self.power = power
        self.energy = energy
        self.avg_speed = avg_speed
        self.max_speed = max_speed

    def __str__(self):
        return super().__str__() + \
               f"평균 파워: {self.power}, 에너지 출력: {self.energy}\n" + \
               f"평균 속도: {self.avg_speed}, 최대 속도: {self.max_speed}"


class Walking(Activity):
    """Walking Activity 클래스 (활동 클래스 중 걷기 클래스)"""

    def __init__(self, sport, date, location, title, description, distance,
                 moving_time, altitude, calory, total_time,
                 pace):

        super().__init__(sport, date, location, title, description, distance,
                 moving_time, altitude, calory, total_time)

        self.pace = pace

    def __str__(self):
        return super().__str__() + f"페이스: {self.pace}"

class Scraper:
    """Scraping 클래스"""

    # 절대 경로로 가져오기
    PATH = os.path.abspath("chromedriver")
    LOGIN_URL = 'http://www.strava.com/login'
    ID = 'kthtim0704@gmail.com'
    PASSWORD = ''
    
    def __init__(self):
        # 크롬 웹드라이버 설정
        self.driver = webdriver.Chrome(self.PATH)

        # 크롬 드라이버 위치 오른쪽으로 붙이기
        self.driver.set_window_position(1920 / 2 + 20, 0)  # 전체 해상도 1920 1080에서 오른쪽 절반으로 x 이동

        # 페이지 로딩이 완료되기까지 몇 초 기다릴지 정하기
        self.driver.implicitly_wait(3)

        # 크롬을 통해 스트라바 접속
        self.driver.get(self.LOGIN_URL)

        self.PASSWORD = pg.password(text='ID : {} 의 비밀번호 입력'
                                    .format(self.ID), title='스트라바 스크레퍼')

        # Activity 모음
        self.activities = []

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
        sleep(0.5)

        # 비밀번호 틀리면 종료
        # if '비밀번호' in self.driver.find_element_by_css_selector('#view_container > div > div > div.pwWryf.bxPAYd > div > div.WEQkZc > div > form > span > section > div > div > div.SdBahf.VxoKGd.Jj6Lae > div.OyEIQ.uSvLId > div:nth-child(2) > span').text:
        #     EC.url_to_be()
        #     sleep(0.5)
        #     self.driver.quit()
        #     return False
        #
        # else:
        #     # 2단계 인증시 처리
        #     # 다시 요청 취소
        #     # self.driver.find_element_by_css_selector('#toggle-c3').click()
        #     return True

        return True

    def make_activity(self):
        """내 활동에서 필요한 데이터 스크레핑"""
        sport = self.driver.find_element_by_css_selector('#heading > header > h2 > span').text
        if '라이딩' in sport:
            sport = '라이딩'
        elif '걷기' in sport:
            sport = '걷기'

        date = self.driver.find_element_by_css_selector('#heading > div > div > div.spans8.activity-summary.mt-md.mb-md > div > div > time').text
        location = self.driver.find_element_by_css_selector('#heading > div > div > div.spans8.activity-summary.mt-md.mb-md > div > div > span').text
        title = self.driver.find_element_by_css_selector('#heading > div > div > div.spans8.activity-summary.mt-md.mb-md > div > div > h1').text
        description = self.driver.find_element_by_css_selector('#heading > div > div > div.spans8.activity-summary.mt-md.mb-md > div > div > div.activity-description-container > div > div > p').text
        distance = self.driver.find_element_by_css_selector('#heading > div > div > div.spans8.activity-stats.mt-md.mb-md > ul:nth-child(1) > li:nth-child(1) > strong').text
        moving_time = self.driver.find_element_by_css_selector('#heading > div > div > div.spans8.activity-stats.mt-md.mb-md > ul:nth-child(1) > li:nth-child(2) > strong').text

        if '라이딩' in sport:
            # 더보기 버튼 클릭
            more_btn = self.driver.find_element_by_css_selector('#heading > div > div.row.no-margins.activity-summary-container > div.spans8.activity-stats.mt-md.mb-md > div.section.more-stats > div:nth-child(1)')
            # 더보기 div가 block 디스플레이라 클릭을 해야하는 경우 클릭
            style = more_btn.get_attribute('style')
            if style == '' or 'block' in style:
                more_btn.find_element('button').click()

            altittude = self.driver.find_element_by_css_selector('#heading > div > div > div.spans8.activity-stats.mt-md.mb-md > ul:nth-child(1) > li:nth-child(3) > strong').text
            calory = self.driver.find_element_by_css_selector('#heading > div > div > div.spans8.activity-stats.mt-md.mb-md > div.section.more-stats > table > tbody.show-more-block-js.hidden > tr > td').text
            # print("calory: {}".format(calory))
            # input()
            total_time = self.driver.find_element_by_css_selector('#heading > div > div > div.spans8.activity-stats.mt-md.mb-md > div.section.more-stats > table > tbody:nth-child(4) > tr > td').text

            power = self.driver.find_element_by_css_selector('#heading > div > div > div.spans8.activity-stats.mt-md.mb-md > ul.inline-stats.section.secondary-stats > li:nth-child(1) > strong').text
            energy = self.driver.find_element_by_css_selector('#heading > div > div > div.spans8.activity-stats.mt-md.mb-md > ul.inline-stats.section.secondary-stats > li:nth-child(2) > strong').text
            avg_speed = self.driver.find_element_by_css_selector('#heading > div > div > div.spans8.activity-stats.mt-md.mb-md > div.section.more-stats > table > tbody:nth-child(2) > tr > td:nth-child(2)').text
            max_speed = self.driver.find_element_by_css_selector('#heading > div > div > div.spans8.activity-stats.mt-md.mb-md > div.section.more-stats > table > tbody:nth-child(2) > tr > td:nth-child(3)').text

            activity = Riding(sport, date, location, title, description, distance, moving_time, altittude, calory, total_time, power, energy, avg_speed, max_speed)

        elif '걷기' in sport:
            # 걷기인 경우
            altittude = self.driver.find_element_by_css_selector('#heading > div > div > div.spans8.activity-stats.mt-md.mb-md > div.section.more-stats > div:nth-child(1) > div:nth-child(2) > strong').text
            calory = self.driver.find_element_by_css_selector('#heading > div > div > div.spans8.activity-stats.mt-md.mb-md > div.section.more-stats > div:nth-child(1) > div:nth-child(4) > strong').text
            total_time = self.driver.find_element_by_css_selector('#heading > div > div > div.spans8.activity-stats.mt-md.mb-md > div.section.more-stats > div:nth-child(2) > div.spans3 > strong').text

            pace = self.driver.find_element_by_css_selector('#heading > div > div > div.spans8.activity-stats.mt-md.mb-md > ul > li:nth-child(3) > strong').text

            activity = Walking(sport, date, location, title, description, distance, moving_time, altittude, calory, total_time, pace)
            # print(activity)
            # input()

        return activity

    def scraping_activities(self):
        """내 활동들 모두 스크래핑 하기"""

        # 로그인 상태 기다리기
        element = WebDriverWait(self.driver, 30).until(
            EC.url_to_be('https://www.strava.com/dashboard#')
        )

        # 내 활동으로 이동
        self.driver.get('https://www.strava.com/athlete/training')
        sleep(0.5)

        # 비공개 체크
        self.driver.find_element_by_css_selector('#search-filters > label:nth-child(2)').click()
        sleep(2)

        while True:
            # 내 활동들 모두 접근해서 정보 가져오기
            # 접근하기 전에 잠시 기다리기
            WebDriverWait(self.driver, 5).until(
                EC.text_to_be_present_in_element((By.CSS_SELECTOR, '.col-title > a'), '배민 알바')
            )

            elements = self.driver.find_elements_by_css_selector('.col-title > a')
            # print(len(elements))

            for element in elements:
                # 새 탭에서 열기
                element.send_keys(Keys.CONTROL + '\n')

            i = len(self.driver.window_handles) - 1
            while i > 0:
                # 새로운 탭으로 초점을 전환
                self.driver.switch_to.window(self.driver.window_handles[i])

                # 새 탭에서 스크래핑하여 필요한 데이터 만들기
                # data = self.driver.find_element_by_css_selector('#heading > div > div')
                # print(data.text)
                self.activities.append(self.make_activity())
                print(self.activities[-1])

                # 현재 탭 종료
                self.driver.close()
                i -= 1

            # 첫번째 탭으로 전환
            # 사용 중인 탭을 닫더라도 초점이 자동으로 이동하지 않아서 다시 전환
            self.driver.switch_to.window(self.driver.window_handles[0])

            next_element = self.driver.find_element_by_css_selector('.next_page')
            # print(next_element.get_attribute('class'))
            if 'disabled' not in next_element.get_attribute('class'):
                next_element.click()
            else:
                break


if __name__ == '__main__':
    scraper = Scraper()

    # 로그인이 성공하면 진행
    if scraper.google_login():
        scraper.scraping_activities()
