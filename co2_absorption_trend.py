import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import numpy as np

# 1. 폰트 경로 찾기
font_path = 'C:/Windows/Fonts/malgun.ttf'  # Windows의 경우 "Malgun Gothic" 폰트 경로
# 2. 폰트 설정
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)
#그래프 DPI 기본값을 변경
plt.rcParams['figure.dpi'] = 100

data = pd.read_csv('Data\년도별 순배출량.csv', low_memory=False)
data2 = data[data['년도']>=2015]

# 그래프 크기 조정
plt.figure(figsize=(15, 5))  # 가로 10인치, 세로 6인치로 설정

# 막대 그래프
bars = plt.bar(data2['년도'], data2['총흡수량'], width=0.8, alpha=0.5, color='green')

# 각 막대 위에 y값 표시
# for bar in bars:
#     yval = bar.get_height()  # 막대의 높이 (y값)
#     plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom')


# 선형 회귀 계산 (1차 다항식)
coefficients = np.polyfit(data2['년도'], data2['총흡수량'], 1)
trendline = np.polyval(coefficients, data2['년도'])

# 추세선 추가
plt.plot(data2['년도'], trendline, color='red', linewidth=2)
plt.legend()
plt.title('산림/초지/기타: 총흡수량 트렌드 (2015년~ 2021년)')
plt.xlabel('년도')
plt.ylabel('온실가스 총흡수량 (k ton-CO2eq)')
plt.show()




