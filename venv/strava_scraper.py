"""
Strava Scraper
selenium을 이용하여 구글 로그인을 한 후
내 Strava 운동 기록 정보에서 원하는 정보를 Scraping 해오기
"""
import json
import os.path
from selenium import webdriver
from time import sleep
import pyautogui as pg
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pickle
import requests
from io import BytesIO
from PIL import Image
import time
import datetime
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter


class Activity:
    """Activity 클래스 (활동 클래스)"""

    def __init__(self, sport, date, location, title, description, delivery_count, distance,
                 moving_time, altitude, calory, total_time):
        self.user = "태훈 김"

        self.sport = sport
        self.date = date
        self.location = location
        self.title = title
        self.description = description
        self.delivery_count = delivery_count
        self.distance = distance
        self.moving_time = moving_time
        self.altitude = altitude
        self.calory = calory
        self.total_time = total_time

    def __str__(self):
        return f"스포츠: {self.sport}, 제목: {self.title}, 날짜: {self.date}, 위치: {self.location}\n" + \
               f"내용: {self.description}, 배달 건수 : {self.delivery_count}, 이동 시간: {self.moving_time}, 고도: {self.altitude}\n" + \
               f"칼로리: {self.calory}, 경과 시간: {self.total_time}\n"

    def dict(self):
        return {
            "sport": self.sport, "date": self.date, "location": self.location, "title": self.title,
            "description": self.description, "delivery_count": self.delivery_count, "distance": self.distance,
            "moving_time": self.moving_time, "altitude": self.altitude, "calory": self.calory,
            "total_time": self.total_time,
        }

    def time_format(self):
        """
            date 데이터(문자열)를 원하는 문자열 형태로 만들기
        """

        # date 데이터(문자열) -> datetime 형태로 변경

        token = self.date.split(' ')

        year = token[0][:-1]
        month = token[1][:-1]
        week = token[2][-4:-3]
        day = token[2][:-6]
        am_pm = token[3]
        hour, minute = token[4].split(':')
        if am_pm == '오후' and int(hour) != 12:
            hour = str(int(hour) + 12)

        dt = datetime.datetime(
            year=int(year), month=int(month), day=int(day),
            hour=int(hour), minute=int(minute))

        self.datetime_format = dt

        w = '월화수목금토일'
        self.time_datetime_format_str = \
            dt.strftime('%y.%m.%d') \
            + f'({w[dt.weekday()]}) {dt.hour:02}:{dt.minute:02}'


class Riding(Activity):
    """Riding Activity 클래스 (활동 클래스 중 라이딩 클래스)"""

    def __init__(self, sport, date, location, title, description, delivery_count, distance,
                 moving_time, altitude, calory, total_time,
                 power, energy, avg_speed, max_speed):
        super().__init__(sport, date, location, title, description, delivery_count, distance,
                         moving_time, altitude, calory, total_time)

        self.power = power
        self.energy = energy
        self.avg_speed = avg_speed
        self.max_speed = max_speed

    def __str__(self):
        return super().__str__() + \
               f"평균 파워: {self.power}, 에너지 출력: {self.energy}\n" + \
               f"평균 속도: {self.avg_speed}, 최대 속도: {self.max_speed}"

    def dict(self):
        dictionary = {"power": self.power, "energy": self.energy, "avg_speed": self.avg_speed,
                      "max_speed": self.max_speed}
        return {**super().dict(), **dictionary}  # 부모 dict과 합쳐서 반환


class Walking(Activity):
    """Walking Activity 클래스 (활동 클래스 중 걷기 클래스)"""

    def __init__(self, sport, date, location, title, description, delivery_count, distance,
                 moving_time, altitude, calory, total_time,
                 pace):
        super().__init__(sport, date, location, title, description, delivery_count, distance,
                         moving_time, altitude, calory, total_time)

        self.pace = pace

    def __str__(self):
        return super().__str__() + f"페이스: {self.pace}"

    def dict(self):
        dictionary = {"pace": self.pace}
        return {**super().dict(), **dictionary}  # 부모 dict과 합쳐서 반환


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

        self.PASSWORD = pg.password(text='ID : {} 의 비밀번호 입력'
                                    .format(self.ID), title='스트라바 스크레퍼')

        # Activity 모음
        self.activities = []

    def google_login(self) -> bool:
        """구글로 로그인"""

        # 크롬을 통해 스트라바 접속
        self.driver.get(self.LOGIN_URL)

        self.driver.find_element_by_css_selector('#login_form > div.google > a').click()
        sleep(0.5)

        # 로그인 아이디 입력
        self.driver.find_element_by_css_selector('#identifierId').send_keys(self.ID)

        # 다음 버튼 클릭
        self.driver.find_element_by_css_selector('#identifierNext > div > button > div.VfPpkd-RLmnJb').click()
        sleep(0.5)

        # 비밀번호 입력
        self.driver.find_element_by_css_selector('#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input').send_keys(
            self.PASSWORD)

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

        date = self.driver.find_element_by_css_selector(
            '#heading > div > div > div.spans8.activity-summary.mt-md.mb-md > div > div > time').text
        location = self.driver.find_element_by_css_selector(
            '#heading > div > div > div.spans8.activity-summary.mt-md.mb-md > div > div > span').text
        title = self.driver.find_element_by_css_selector(
            '#heading > div > div > div.spans8.activity-summary.mt-md.mb-md > div > div > h1').text
        description_str = self.driver.find_element_by_css_selector(
            '#heading > div > div > div.spans8.activity-summary.mt-md.mb-md > div > div > div.activity-description-container > div > div > p').text
        descriptions = description_str.split('\n')
        delivery_count = descriptions[0]  # 내용에서 배달 건수 분리
        description = ""
        # 내용이 따로 있으면 추가
        if len(descriptions) > 1:
            description = descriptions[1]

        distance = self.driver.find_element_by_css_selector(
            '#heading > div > div > div.spans8.activity-stats.mt-md.mb-md > ul:nth-child(1) > li:nth-child(1) > strong').text
        moving_time = self.driver.find_element_by_css_selector(
            '#heading > div > div > div.spans8.activity-stats.mt-md.mb-md > ul:nth-child(1) > li:nth-child(2) > strong').text

        if '라이딩' in sport:
            # 더보기 버튼 클릭
            more_btn = self.driver.find_element_by_css_selector(
                '#heading > div > div.row.no-margins.activity-summary-container > div.spans8.activity-stats.mt-md.mb-md > div.section.more-stats > div:nth-child(1)')
            # 더보기 div가 block 디스플레이라 클릭을 해야하는 경우 클릭
            style = more_btn.get_attribute('style')
            if style == '' or 'block' in style:
                more_btn.find_element_by_css_selector('button').click()

            altitude = self.driver.find_element_by_css_selector(
                '#heading > div > div > div.spans8.activity-stats.mt-md.mb-md > ul:nth-child(1) > li:nth-child(3) > strong').text
            calory = self.driver.find_element_by_css_selector(
                '#heading > div > div > div.spans8.activity-stats.mt-md.mb-md > div.section.more-stats > table > tbody.show-more-block-js.hidden > tr > td').text
            # print("calory: {}".format(calory))
            # input()
            total_time = self.driver.find_element_by_css_selector(
                '#heading > div > div > div.spans8.activity-stats.mt-md.mb-md > div.section.more-stats > table > tbody:nth-child(4) > tr > td').text

            power = self.driver.find_element_by_css_selector(
                '#heading > div > div > div.spans8.activity-stats.mt-md.mb-md > ul.inline-stats.section.secondary-stats > li:nth-child(1) > strong').text
            energy = self.driver.find_element_by_css_selector(
                '#heading > div > div > div.spans8.activity-stats.mt-md.mb-md > ul.inline-stats.section.secondary-stats > li:nth-child(2) > strong').text
            avg_speed = self.driver.find_element_by_css_selector(
                '#heading > div > div > div.spans8.activity-stats.mt-md.mb-md > div.section.more-stats > table > tbody:nth-child(2) > tr > td:nth-child(2)').text
            max_speed = self.driver.find_element_by_css_selector(
                '#heading > div > div > div.spans8.activity-stats.mt-md.mb-md > div.section.more-stats > table > tbody:nth-child(2) > tr > td:nth-child(3)').text

            activity = Riding(sport, date, location, title, description, delivery_count, distance, moving_time,
                              altitude, calory, total_time, power, energy, avg_speed, max_speed)

        elif '걷기' in sport:
            # 걷기인 경우
            altitude = self.driver.find_element_by_css_selector(
                '#heading > div > div > div.spans8.activity-stats.mt-md.mb-md > div.section.more-stats > div:nth-child(1) > div:nth-child(2) > strong').text
            calory = self.driver.find_element_by_css_selector(
                '#heading > div > div > div.spans8.activity-stats.mt-md.mb-md > div.section.more-stats > div:nth-child(1) > div:nth-child(4) > strong').text
            total_time = self.driver.find_element_by_css_selector(
                '#heading > div > div > div.spans8.activity-stats.mt-md.mb-md > div.section.more-stats > div:nth-child(2) > div.spans3 > strong').text

            pace = self.driver.find_element_by_css_selector(
                '#heading > div > div > div.spans8.activity-stats.mt-md.mb-md > ul > li:nth-child(3) > strong').text

            activity = Walking(sport, date, location, title, description, delivery_count, distance, moving_time,
                               altitude, calory, total_time, pace)
            # print(activity)
            # input()

        # 내가 원하는 형태의 데이터 포맷 만들어 두기
        activity.time_format()

        return activity

    def download_user_img(self):
        sleep(0.5)
        # 이렇게하면 medium.jpg 이미지 가져옴
        img_url = self.driver.find_element_by_css_selector(
            '#container-nav > ul.user-nav.nav-group > li.nav-item.drop-down-menu.user-menu.enabled > a > div > img').get_attribute(
            'src')
        img_url = img_url[:img_url.rfind('/')] + '/large.jpg'  # large 이미지로 변경

        # print(img_url)
        # input()

        # 이미지 요청 및 다운로드
        res = requests.get(img_url)
        img = Image.open(BytesIO(res.content))
        img.save("./Resources/user.jpg", "JPEG")

    def scraping_all_activities(self):
        """내 활동들 모두 스크래핑 하기"""

        # 로그인 상태 기다리기
        element = WebDriverWait(self.driver, 30).until(
            EC.url_to_be('https://www.strava.com/dashboard#')
        )

        # 유저 이미지 다운 받기
        self.download_user_img()

        # 내 활동으로 이동
        self.driver.get('https://www.strava.com/athlete/training')
        sleep(0.5)

        # 비공개 체크
        self.driver.find_element_by_css_selector('#search-filters > label:nth-child(2)').click()
        sleep(3)

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

        # 웹드라이버 종료
        self.driver.quit()  # 모든 webdriver 종료 close는 현재 활성화된거만 종료

    def save_activity(self):
        """활동들 json 파일로 저장하기"""

        activities_json = {'activity': []}

        for activity in self.activities:
            activities_json['activity'].append(activity.dict())

        with open('./Resources/activities.json', 'w') as json_file:
            json.dump(activities_json, json_file, ensure_ascii=False, indent='\t')

    def load_activitiy(self):
        """활동들 json 파일로 읽어오기"""
        self.activities.clear()  # activities 비우기

        with open('./Resources/activities.json', 'r') as json_file:
            activities_json = json.load(json_file)

        for activity_dict in activities_json['activity']:
            # print(activity)

            if activity_dict['sport'] == '라이딩':
                activity = Riding(activity_dict['sport'], activity_dict['date'],
                                  activity_dict['location'], activity_dict['title'],
                                  activity_dict['description'], activity_dict['delivery_count'],
                                  activity_dict['distance'], activity_dict['moving_time'],
                                  activity_dict['altitude'], activity_dict['calory'],
                                  activity_dict['total_time'], activity_dict['power'],
                                  activity_dict['energy'], activity_dict['avg_speed'], activity_dict['max_speed'])
            elif activity_dict['sport'] == '걷기':
                activity = Walking(activity_dict['sport'], activity_dict['date'],
                                   activity_dict['location'], activity_dict['title'],
                                   activity_dict['description'], activity_dict['delivery_count'],
                                   activity_dict['distance'], activity_dict['moving_time'],
                                   activity_dict['altitude'], activity_dict['calory'],
                                   activity_dict['total_time'], activity_dict['pace'])

            activity.time_format()

            self.activities.append(activity)

    def time_to_second(self, time_format) -> int:
        """time 포맷을 second로 변경"""

        # print(time_format)

        time_tokens = time_format.split(':')
        if len(time_tokens) == 2:
            hour = 0
            minute = time_tokens[0]
            second = time_tokens[1]
        else:
            hour = time_tokens[0]
            minute = time_tokens[1]
            second = time_tokens[2]

        return int(hour) * 3600 + int(minute) * 60 + int(second)

    def second_to_time(self, second) -> str:
        """sconde를 time 포맷으로 변경"""

        hour = second // 3600
        minute = (second % 3600) // 60
        second = second % 60

        return '{}:{:02}:{:02}'.format(hour, minute, second)

    def total_activity(self):
        """활동들의 누적 데이터 값 반환하기"""

        last_date = self.activities[0].time_datetime_format_str
        first_date = self.activities[-1].time_datetime_format_str

        sum_distance = 0
        sum_altitude = 0
        sum_delivery_count = 0

        # 시간은 모두 초로 변경 후 계산 후 다시 시,분,초로 변경
        sum_total_time = 0
        sum_moving_time = 0

        activity_count = len(self.activities)
        activity_ride_count = 0
        activity_walk_count = 0

        for activity in self.activities:
            if activity.sport == '라이딩':
                activity_ride_count += 1
            else:
                activity_walk_count += 1

            sum_distance += float(activity.distance[:-2])
            sum_altitude += int(activity.altitude[:-1])
            sum_delivery_count += int(activity.delivery_count)

            sum_total_time += self.time_to_second(activity.total_time)
            sum_moving_time += self.time_to_second(activity.moving_time)

        sum_total_time_str = self.second_to_time(sum_total_time)
        sum_moving_time_str = self.second_to_time(sum_moving_time)

        # print('활동 기간 : {} ~ {}'.format(first_date, last_date))
        # print('누적 전체 시간 : {}'.format(sum_total_time_str))
        # print('누적 이동 시간 : {}'.format(sum_moving_time_str))
        # print('누적 이동 거리 : {:.2f}km'.format(sum_distance))
        # print('누적 고도 : {}m'.format(sum_altitude))
        # print('총 배달 건수 : {}건'.format(sum_delivery_count))
        # print('총 배민 활동 횟수 : {}건'.format(activity_count))
        # print('총 배민 활동 도보 횟수 : {}건'.format(activity_walk_count))
        # print('총 배민 활동 자전거 횟수 : {}건'.format(activity_ride_count))

        return {
            "total_date": '활동 기간 \n{} ~ {}'.format(first_date, last_date),
            "sum_total_time": '누적 전체 시간\n {}'.format(sum_total_time_str),
            "sum_moving_time": '누적 이동 시간\n {}'.format(sum_moving_time_str),
            "sum_distance": '누적 이동 거리\n {:.2f}km'.format(sum_distance),
            "sum_altitude": '누적 고도\n {}m'.format(sum_altitude),
            "sum_delivery_count": '총 배달 건수\n {}건'.format(sum_delivery_count),
            "activity_count": '총 배민 활동 횟수\n {}건'.format(activity_count),
            "activity_walk_count": '총 배민 활동 도보 횟수\n {}건'.format(activity_walk_count),
            "activity_ride_count": '총 배민 활동 자전거 횟수\n {}건'.format(activity_ride_count),
        }

    def make_graph(self, date_list, delivery_list, file_name):
        """일별 배달건수 그래프를 만들어 저장하기"""

        # matplotlib 이용해서 데이터 시각화 하기
        plt.figure(figsize=(13, 8))

        # 한글 폰트 설정
        font_path = './BMJUA_ttf.ttf'  # 폰트 경로
        # font_path = 'C:/Users/Kay/PycharmProjects/Strava_Pyton_WebCrawling/venv/BMJUA_ttf.ttf'
        font_prop = fm.FontProperties(fname=font_path)  # FontProperties 인스턴스 생성
        font_name = font_prop.get_name()  # 폰트 이름
        plt.rc('font', family=font_name)  # 폰트 일괄 설정

        if 'total' in file_name:
            plt.title('전체 배달 건수 통계')
        else:
            plt.title(f'{date_list[0].year}년 {date_list[0].month}월 배달 건수 통계')
        plt.xlabel('날짜')
        plt.ylabel('배달 건수')

        plt.grid()

        # plt.scatter(date_list, delivery_list)
        # plt.plot(date_list, delivery_list, marker='o')
        # plt.bar(date_list, delivery_list)

        plt.plot_date(date_list, delivery_list)

        axes = plt.gca()
        formatter = DateFormatter('%y.%m.%d')
        axes.xaxis.set_major_formatter(formatter)
        plt.xticks(rotation=25)

        if 'total' not in file_name:
            plt.xticks(rotation=90)
            axes.xaxis.set_major_locator(mdates.DayLocator())

        # 주석 표시
        # 전체 통계의 경우 시작 배달일 추가
        if 'total' in file_name:
            start_ann = plt.annotate(f'시작일 [{date_list[0].strftime("%y.%m.%d")} : {delivery_list[0]}건]',
                                     xy=(mdates.date2num(date_list[0]), delivery_list[0]), xytext=(-100, 15),
                                     textcoords='offset points', arrowprops=dict(arrowstyle='-|>'),
                                     bbox=dict(boxstyle='round', facecolor='violet', alpha=0.5))

        # print(delivery_list)
        max_delivery_count = max(delivery_list)
        # print(max_delivery_count)
        max_delivery_date = date_list[delivery_list.index(max_delivery_count)]

        max_delivery_ann = plt.annotate(f'최대 배달일 [{max_delivery_date.strftime("%y.%m.%d")} : {max_delivery_count}건]',
                                        xy=(mdates.date2num(max_delivery_date), max_delivery_count), xytext=(10, 10),
                                        textcoords='offset points', arrowprops=dict(arrowstyle='-|>'),
                                        bbox=dict(boxstyle='round', facecolor='dodgerblue', alpha=0.5))

        avg_delivery_count = sum(delivery_list) // len(delivery_list)
        # print(avg_delivery_count)

        avg_delivery_text = plt.text(0.85, 1.05, f'평균 배달 건수 : {avg_delivery_count}건', fontsize=12,
                                    transform=axes.transAxes, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        plt.savefig('./Resources/Graphs/' + file_name)
        # plt.show()

        # start_ann.remove()
        # max_delivery_ann.remove()

    def divide_date(self, date_list, delivery_list):
        """전체 데이터 월별로 나누기"""
        start_year, start_month = date_list[0].year, date_list[0].month
        end_year, end_month = date_list[-1].year, date_list[-1].month

        period = []
        year, month = start_year, start_month
        while True:
            period.append((year, month))

            if year == end_year and month == end_month:
                break

            month += 1
            if month == 13:
                month = 1
                year += 1

        # print(period)

        result = []

        for year, month in period:
            res_list = list(filter(lambda x: date_list[x].year == year and date_list[x].month == month, range(len(date_list))))
            # print(res_list)

            divide_date_list = []
            divide_delivery_list = []

            for res in res_list:
                # print(f'{date_list[res]} : {delivery_list[res]}')
                divide_date_list.append(date_list[res])
                divide_delivery_list.append(delivery_list[res])

            result.append((divide_date_list, divide_delivery_list, f'{year}_{month}_graph.png'))

        return result

    def make_delivery_statistics(self):
        """일별 배달건수 통계 만들기"""

        date_list = []
        delivery_list = []

        for activity in reversed(self.activities):
            # print(f'{activity.datetime_format} : {activity.delivery_count}')

            date_list.append(activity.datetime_format)
            # date_list.append(activity.datetime_format)
            delivery_list.append(int(activity.delivery_count))

        self.make_graph(date_list, delivery_list, "total_graph.png")  # 전체 통계 먼저 처리

        divide_date_list = self.divide_date(date_list, delivery_list)

        # print(divide_date_list)
        # input()

        for monthly_date, monthly_delivery, file_name in divide_date_list:
            self.make_graph(monthly_date, monthly_delivery, file_name)


if __name__ == '__main__':
    scraper = Scraper()

    # 로그인이 성공하면 진행
    # if scraper.google_login():
    #     scraper.scraping_all_activities()

    # 파일로 저장하기
    # if len(scraper.activities) > 0:
    #     scraper.save_activity()

    # 파일로 읽어오기
    scraper.driver.quit()
    scraper.load_activitiy()

    # 누적 데이터 확인
    # scraper.total_activity()

    # 일별 배달건수 통계 만들기
    scraper.make_delivery_statistics()
