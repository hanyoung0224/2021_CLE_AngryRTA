# A* 알고리즘을 활용한 최소 연비 경로 탐색 알고리즘
###### 포산고등학교 2021학년도 CLE: 앵그리RTA 아이디어 프로토타입

---
### 알고리즘 개요
특정 속력으로 정속주행을 가정한 뒤 차량의 연료 소모량을 가중치로 하여 변형된 A* 알고리즘을 적용함.
주어진 그래프의 각 교차로에는 신호가 설정되어 있고, 차량이 신호에 걸리면 다음 세 가지 값 중 가장 작은 값을 G 값으로 선택함.

- 이전 교차로에서 현재 교차로까지 속력을 높여 신호에 맞춰 교차로를 지날 때, (이전 교차로까지의 연료 소모량) + (증가한 연비에 의한 연료 소모량) + (다음 교차로까지 원래 속력으로 주행할 때 연료 소모량) + (가속에 의해 증가한 운동 에너지를 공급하기 위한 연료 소모량)
- 이전 교차로에서 현재 교차로까지 속력을 늦춰 신호에 맞춰 교차로를 지날 때, (이전 교차로까지의 연료 소모량) + (증가한 연비에 의한 연료 소모량) + (다음 교차로까지 원래 속력으로 주행할 때 연료 소모량) + (감속 상태에서 원래 속력으로 가속할 때 증가한 운동 에너지를 공급하기 위한 언료 소모량)
- 이전 교차로에서 현재 교차로까지 원래 속력으로 주행할 때, (현재 교차로까지의 연료 소모량) + (다음 교차로까지 원래 속력으로 주행할 때 연료 소모량) + (정지 상태에서 원래 속력으로 차량을 가속할 때 증가한 운동 에너지를 공급하기 위한 연료 소모량)

---
### 알고리즘 구현에 사용된 상수

- 표준 속력: 20.3987686 m/s (연비 함수가 최소일 때의 속력)
- 연비 함수: 속력이 x m/s일 때, 연비 y = 2285.93762 + 132.7298916 * x - 0.251032407 * (x ** 2) m/L
- 차량의 질량: 1510 kg (포르쉐 911 공차 중량 기준)
- 엔진의 열효율: 0.38
- 휘발유의 리터당 에너지: 32.6 MJ/L