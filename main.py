from selenium import webdriver
from selenium.webdriver.chrome.service import Service

import chromedriver_autoinstaller
import subprocess
import time

# 디버그 크롬 구동
subprocess.Popen(r'./Application/chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"')  

# 크롬 옵션 설정
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--incognito')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("disable-blink-features=AutomationControlled")  # 자동화 탐지 방지
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36")
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

# 크롬 버전 확인
chrome_version = chromedriver_autoinstaller.get_chrome_version().split('.')[0] 

# 크롬드라이버 경로 설정
chrome_directory = f'./{chrome_version}/chromedriver.exe'

# 크롬드라이버 실행
service = Service(executable_path=chrome_directory)
try:
    driver = webdriver.Chrome(service=service, options=chrome_options)
except:
    chromedriver_autoinstaller.install(True)
    driver = webdriver.Chrome(service=service, options=chrome_options)

driver.implicitly_wait(20)

mode = 0  # 작동 방식 설정 (0: URL 조회 전략, 1: 새창 열기 전략, 2: 리프레시 전략)

url_count = 3  # 조회수를 조작할 URL 개수
url_delay = 3  # URL 조회 간격 (초)

open_url = 'https://www.campuspick.com/activity/view?id=26203'  # 실제 조회수를 조작할 URL
prev_url = 'https://www.campuspick.com/activity'  # 재열람 전략일 경우 해당 게시물을 접근하기 전 주소를 입력합니다.


def viewProcess():
    for i in range(0, url_count):
        driver.execute_script(f'window.open("{open_url}");')
        
    time.sleep(url_delay)

    tabs = driver.window_handles

    for i in range(1, len(tabs)):
        driver.switch_to.window(tabs[i])
        driver.delete_all_cookies()
        driver.close()

    time.sleep(url_delay)

    driver.switch_to.window(tabs[0])

    viewProcess()


def newTabProcess():
    for i in range(0, url_count):
        driver.execute_script('window.open("about:blank", "_blank");')

    time.sleep(url_delay)

    tabs = driver.window_handles

    for i in range(0, url_count):
        driver.switch_to.window(tabs[i])
        driver.get(f'{prev_url}')
        driver.get(f'{open_url}')
        
    newTabRepeat()


def newTabRepeat():
    tabs = driver.window_handles
    
    for i in range(0, url_count):
        driver.switch_to.window(tabs[i])
        driver.back()

    time.sleep(3)

    for i in range(0, url_count):
        driver.switch_to.window(tabs[i])
        driver.forward()
        driver.delete_all_cookies()

    newTabRepeat()

def refreshProcess():
    driver.refresh()
    time.sleep(3)
    refreshProcess()

if mode == 2:
    refreshProcess()

if mode == 1:
    newTabProcess()

elif mode == 0: 
    viewProcess()
