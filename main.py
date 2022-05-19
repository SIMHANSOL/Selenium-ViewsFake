from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import subprocess
import time

subprocess.Popen(
    r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"')  # 디버거 크롬 구동

option = Options()
option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
option.add_argument('--incognito')

chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[
    0]  # 크롬드라이버 버전 확인
try:
    driver = webdriver.Chrome(
        f'./{chrome_ver}/chromedriver.exe', options=option)
except:
    chromedriver_autoinstaller.install(True)
    driver = webdriver.Chrome(
        f'./{chrome_ver}/chromedriver.exe', options=option)

driver.implicitly_wait(20)

mode = 1  # 작동 방식 설정 (0: URL 열기 전략, 1: 재열람 전략)
open_url = ''  # 실제 조회수를 조작할 URL
prev_url = ''  # 재열람 전략일 경우 해당 게시물을 접근하기 전 주소를 입력합니다.


def openURL():
    driver.execute_script(f'window.open("{open_url}");')
    driver.execute_script(f'window.open("{open_url}");')
    driver.execute_script(f'window.open("{open_url}");')
    driver.execute_script(f'window.open("{open_url}");')
    driver.execute_script(f'window.open("{open_url}");')
    time.sleep(5)

    tabs = driver.window_handles

    driver.switch_to.window(tabs[5])
    driver.close()
    driver.switch_to.window(tabs[4])
    driver.close()
    driver.switch_to.window(tabs[3])
    driver.close()
    driver.switch_to.window(tabs[2])
    driver.close()
    driver.switch_to.window(tabs[1])
    driver.close()
    driver.switch_to.window(tabs[0])
    openURL()


def readyRepeatURL(index):
    driver.switch_to.window(tabs[index])
    driver.get(f'{prev_url}')
    driver.get(f'{open_url}')


def repeatURL():
    driver.switch_to.window(tabs[0])
    driver.back()
    driver.switch_to.window(tabs[1])
    driver.back()
    driver.switch_to.window(tabs[2])
    driver.back()
    driver.switch_to.window(tabs[0])
    driver.forward()
    driver.switch_to.window(tabs[1])
    driver.forward()
    driver.switch_to.window(tabs[2])
    driver.forward()
    repeatURL()


if mode == 1:
    driver.execute_script('window.open("about:blank", "_blank");')
    driver.execute_script('window.open("about:blank", "_blank");')

    time.sleep(5)

    tabs = driver.window_handles

    readyRepeatURL(0)
    readyRepeatURL(1)
    readyRepeatURL(2)
    repeatURL()
elif mode == 0:
    openURL()
