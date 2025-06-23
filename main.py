from selenium import webdriver
from selenium.webdriver.chrome.service import Service

import chromedriver_autoinstaller
import subprocess
import time
import os

# NOTE: Application 폴더의 Chrome 버전에 맞춘 설정
application_chrome_version = '126'
chrome_executable_path = './Application/chrome.exe'

# 디버그 크롬 구동 (기존 프로세스 종료 후 실행)
try:
    # NOTE: 기존 Chrome 프로세스 종료
    subprocess.run('taskkill /f /im chrome.exe', shell=True, capture_output=True)
    time.sleep(2)
except:
    # NOTE: Chrome 프로세스가 없는 경우 무시
    pass

# NOTE: Chrome 실행 파일 경로 확인
if not os.path.exists(chrome_executable_path):
    print(f'Chrome 실행 파일을 찾을 수 없습니다: {chrome_executable_path}')
    exit(1)

# NOTE: 디버그 모드로 Chrome 실행
subprocess.Popen(f'{chrome_executable_path} --remote-debugging-port=9222 --user-data-dir="C:\\chrometemp"')
time.sleep(3)

# 크롬 옵션 설정
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--incognito')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("disable-blink-features=AutomationControlled")  # 자동화 탐지 방지
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36")
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

# 크롬 버전 확인 (Application 폴더 버전 사용)
chrome_version = application_chrome_version

# 크롬드라이버 경로 설정
chrome_directory = f'./{chrome_version}/chromedriver.exe'

# NOTE: ChromeDriver 존재 확인
if not os.path.exists(chrome_directory):
    print(f'ChromeDriver를 찾을 수 없습니다: {chrome_directory}')
    print('올바른 버전의 ChromeDriver를 다운로드합니다...')
    # NOTE: 126 버전용 ChromeDriver 자동 설치
    try:
        # 126 버전 폴더가 없으면 생성
        if not os.path.exists(f'./{chrome_version}'):
            os.makedirs(f'./{chrome_version}')
        
        # NOTE: ChromeDriver 자동 설치 (기본 경로에 설치 후 이동)
        installed_path = chromedriver_autoinstaller.install()
        
        # NOTE: 설치된 ChromeDriver를 버전 폴더로 복사
        if installed_path and os.path.exists(installed_path):
            import shutil
            shutil.copy2(installed_path, chrome_directory)
            print(f'ChromeDriver를 {chrome_directory}로 복사했습니다.')
        else:
            # NOTE: 기존 137 버전을 임시로 사용
            if os.path.exists('./137/chromedriver.exe'):
                import shutil
                shutil.copy2('./137/chromedriver.exe', chrome_directory)
                print(f'기존 ChromeDriver를 {chrome_directory}로 복사했습니다.')
            else:
                raise Exception('ChromeDriver를 찾을 수 없습니다.')
                
    except Exception as error:
        print(f'ChromeDriver 설치 중 오류 발생: {error}')
        exit(1)

# 크롬드라이버 실행
service = Service(executable_path=chrome_directory)
try:
    driver = webdriver.Chrome(service=service, options=chrome_options)
    print('Chrome WebDriver 연결 성공!')
except Exception as error:
    print(f'Chrome WebDriver 연결 실패: {error}')
    try:
        print('ChromeDriver 재설치를 시도합니다...')
        # NOTE: ChromeDriver 재설치
        installed_path = chromedriver_autoinstaller.install()
        if installed_path and os.path.exists(installed_path):
            import shutil
            shutil.copy2(installed_path, chrome_directory)
        
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print('Chrome WebDriver 연결 성공!')
    except Exception as retry_error:
        print(f'재시도 후에도 연결 실패: {retry_error}')
        exit(1)

driver.implicitly_wait(20)

mode = 0  # 작동 방식 설정 (0: URL 조회 전략, 1: 새창 열기 전략, 2: 리프레시 전략)

url_count = 3  # 조회수를 조작할 URL 개수
url_delay = 1  # URL 조회 간격 (초)

open_url = 'https://www.campuspick.com/activity/view?id=29614'  # 실제 조회수를 조작할 URL
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
    time.sleep(1)
    refreshProcess()

if mode == 2:
    refreshProcess()

if mode == 1:
    newTabProcess()

elif mode == 0: 
    viewProcess()
