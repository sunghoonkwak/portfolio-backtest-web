# 포트폴리오별 backtesting을 위한 web page 만들기

## 1. 목적
This is for making web page for asset backtesting

## 2. html page 설명
1. html page는 index.html로 구성된다.
 - 페이지는 가로로 2개의 section으로 구성된다.
 - 왼쪽 section은 backtesting period, portfolio manager table, buttons 순서로 구성된다. size 45%로 설정한다.
 - 오른쪽 section은 backtesting result를 표시하는 section으로 구성된다. size 55%로 설정한다.

## 3. 기간 입력용 form 설명
1. form은 start date, end date로 구성 되며 가로 방향으로 배치된다.
  - start date와 end date는 calendar로 선택할 수 있다.
    >> start date는 end date 보다 빠른 날짜만 선택이 가능하다.
    >> end date는 페이지를 사용하는 현재 날짜 이전의 날짜만 선택이 가능하다.
  - default end date는 페이지를 사용하는 현재 날짜의 하루전날, start date는 default end date의 1년 전 날짜로 설정된다.

## 4. portfolio manager table 설명
1. 테이블은 default.json을 읽어서 만든다.
2. 테이블은 ticker, name, 포트폴리오별 weight로 구성된다. ticker칸은 name칸의 절반크기로 설정한다.
  - ticker별 check box가 표시되며, check box의 data는 ticker의 수익률을 표시 여부를 나타낸다.
3. ticker는 입력가능한 셀, name은 수정 불가능한 셀, 포트폴리오별 weight는 수정 가능한 셀이다.
  - 포트폴리오별 weight는 0%에서 100% 사이의 값을 가져야 한다. 최소단위는 0.01%이며, 모든 수치는 소수점 둘째 자리까지 표기된다. (예: 10.00%) (입력 가독성을 위해 up/down 버튼은 제거되었으며, 필드 우측에 % 단위가 표시된다.)
4. ticker에 "USD"나 "KRW"를 입력하면, name은 "cash"로 표시된다.
5. 테이블의 맨 아래에는 ticker는 입력불가한 공란, name은 "total", 포트폴리오별 weight는 수정불가능한 셀에 포트폴리오별 weight의 합이 표시된다.
6. 각 portfolio의 rebalance interval을 선택할 수 있는 drop box가 테이블 헤더 영역에 표시된다.
  - weekly, monthly, quarterly, yearly, none으로 구성되며 default는 monthly로 설정된다.

## 5. Buttons 설명
1. "+ portfolio", "+ ticker", "load", "save", "backtest" 버튼을 생성한다.
  - "+ portfolio" 버튼을 누르면 가로로 한 줄 추가되어 2개 이상의 포트폴리오를 입력할 수 있게 된다.
    >> 각 포트폴리오를 삭제할 수 있는 x버튼이 각각의 portfolio에 제공되어야하며, 1개의 portfolio만 존재할 경우 x버튼을 눌러도 삭제되지 않는다.
    >> 각 포트폴리오의 이름도 수정이 가능해야한다.
  - "+ ticker" 버튼을 누르면 table이 한 줄 추가된다. ticker를 입력하면, name은 ticker.json을 읽어서 결정된다.
    >> ticker.json에 정보가 존재하지 않는다면 ticker.py를 통해서 실시간으로 정보를 가져오며 ticker.json을 업데이트 한다. (사용자 경험을 위해 백그라운드에서 자동으로 정보를 조회하고 동기화한다.)
  - "load" 버튼을 누르면 JSON 파일을 읽어서 기간 및 테이블 내용을 복구한다. JSON 파일은 default.json과 같은 구조를 가져야한다.
    >> 반영할 내용을 선택하는 popup이 생성된다. popup을 통해서 기간, 포트폴리오, Ticker별 체크박스 상태를 선택적으로 반영 할 수 있다.
    >> 기간을 선택하면 기간은 override 된다.
    >> 포트폴리오를 선택하면 해당 포트폴리오들이 기존 테이블의 포트폴리오 리스트 뒤에 추가(append) 된다. 이때 로드된 데이터의 ticker를 기존 정보와 비교하여 name이 다르면 올바른 연동 정보로 자동 업데이트(동기화) 한다. 정보가 없는 ticker는 백그라운드에서 정보를 가져와 업데이트한다.
  - "save" 버튼을 누르면 현재 설정(기간, 포트폴리오별 주기, 종목 및 비중)이 포함된 JSON 파일이 다운로드된다.
    >> 모든 포트폴리오의 weight의 합이 100%가 되지 않아도 save를 할 수 있다.
  - "backtest" 버튼을 누르면 backtesting을 실행한다.
    >> 모든 포트폴리오의 weight의 합이 100%가 되지 않으면 남은 weight를 cash로 반영할 지에 대해 묻는 popup이 생성된다. 수락하면 cash에 반영하고 backtesting을 실행 여부를 다시 묻는다. 거절하면 backtesting을 실행하지 않는다.
    >> 모든 포트폴리오의 weight의 합이 100%를 초과하면 전체 종목의 비중을 동일 비율로 조정하여 100%로 만들지 묻는 popup이 생성된다. 수락하면 변경 후 실행 여부를 다시 묻는다. 거절하면 backtesting을 실행하지 않는다.

## 6. backtesting 결과
1. backtesting 결과는 html page의 오른쪽 section에 표시된다.
2. backtesting 결과는 아래와 같이 표시한다.
  - 각 포트폴리오의 최종 수익률과 표준편차를 table로 표시한다.
    >> check box가 체크되어있는 ticker의 수익률도 함께 표시한다.
  - 투자기간 동안의 수익률 그래프를 표시한다. 가로축은 날짜를 나타내고, 세로축은 수익률을 나타낸다.
    >> check box가 체크되어있는 ticker의 수익률도 함께 표시한다.
3. 결과 download 버튼이 하단부에 배치되며, 모든 결과를 포함한 Excel 파일(.xlsx)이 다운로드된다.
4. check box가 체크되면 해당 ticker의 기간동안의 수익률을 그래프에 추가로 표시한다.

## 7. tools
1. python
2. html

## 8. file name 및 상세 로직
1. main python file: main.py
2. ticker_searching python file: ticker.py 
  - yfinance를 사용하여 ticker의 정보를 가져와서 ticker.json을 업데이트 한다.
  - 이 파일만 ticker.json을 수정할 수 있다.
3. backtesting python file: backtest.py
  - yfinance를 사용하여 필요한 ticker의 price data를 얻어온다.
  - 각각의 포트폴리오의 weight 및 독립적인 rebalance 주기(interval)에 따라 backtesting을 실행한다.
  - 시작일의 수익률은 0%이다.
  - rebalance 기준은 weekly, monthly, quarterly, yearly의 실제 마지막 거래일(Last Trading Day) 종가 기준이다.
  - daily 수익률 변화, rebalancing history를 하나의 excel 파일로 저장한다.
    >> excel file font는 10, 모든 열 너비는 20으로 설정한다.
    >> daily 수익률 변화 시트와 각 포트폴리오명으로 된 rebalancing history 시트들로 구성된다.
    >> rebalancing history 시트에는 rebalancing day, 시작일(100%) 대비 누적 수익률이 반영된 총 가치(%), 종목별 리밸런싱 전/후 가치(%)가 기록된다.
  - cash의 daily 수익률은 0%이다.
4. html file: index.html
5. default portfolio json file: default.json (전역 config 및 포트폴리오별 상세 설정 포함)
6. ticker list json file: ticker.json
