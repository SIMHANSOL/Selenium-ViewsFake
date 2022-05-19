# Selenium_ViewsFake

#### 셀레니움 학습용 <br>
셀레니움을 이용한 조회수 조작 기능 예제입니다.

<br>

## Install
``` sh
$ pip install selenium
$ pip install chromedriver-autoinstaller
```

<br>

## Use
``` sh
$ py main.py
```

<br>

## Options
``` sh
mode = 1  # 작동 방식 설정 (0: URL 열기 전략, 1: 재열람 전략)
open_url = ''  # 실제 조회수를 조작할 URL
prev_url = ''  # 재열람 전략일 경우 해당 게시물을 접근하기 전 주소를 입력합니다.
```

<br>

## Information
웹사이트의 게시물 조회수를 조작합니다.

웹사이트마다 조회수 처리 방식이 다르기 때문에 조작하고자 하는 웹사이트가 조회수를 어떻게 처리하는지 알아볼 필요가 있습니다.

조작하고자 하는 웹사이트의 방식에 따라 셀레니움을 조작해야 합니다.

실제 조회수를 마케팅 수단으로 활용할 수 있는 사이트를 참고하여 2가지 방식을 제작하였습니다.

### * URL 열기 전략, 재열람 전략
```
1. 이전 라우트 검증을 통해 조회수 처리(링XXX)
[재열람 전략 사용]

2. 쿠키, 세션, IP 검증을 통해 조회수 처리(이XXX)
[URL 열기 전략 사용]

3. 검증이 없어, 페이지를 열람하거나 또는 해당 주소로 트래픽만 보내도 조회수 처리(캠XXX)
[URL 열기 전략, 재열람 전략 사용]
```

### * 조회수 처리 방식
조회수가 오른 것처럼 보이지만 실제 반영이 안된 경우가 많은데 DB 부하를 방지하기 위해 아래 2번을 사용하고 있을 확률이 높으며 대다수는 일정 시간 이후 적용됩니다.
```
1. 페이지 열람시 바로 조회수 UPDATE
2. 페이지 열람시 임시 메모리에 저장, 특정 시간에 조회수 UPDATE
```
