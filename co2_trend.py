import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

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
plt.figure(figsize=(15, 7))  # 가로 10인치, 세로 6인치로 설정

# 선그래프
plt.plot(data['년도'], data['순배출량'], color='orange', linewidth=4, label='순배출량', alpha=0.8)
plt.plot(data['년도'], data['총배출량'], color='grey', linewidth=2, label='총배출량', linestyle='--', alpha=0.6)
plt.plot(data['년도'], data['총흡수량'], color='green', linewidth=2, label='총흡수량', linestyle='--', alpha=0.6)

plt.legend()
plt.xlabel('년도')
plt.ylabel('k ton-CO2eq')
# 모든 x축 tick 표시
plt.xticks(data['년도'])  # x의 모든 값을 x축 눈금으로 설정
plt.show()




