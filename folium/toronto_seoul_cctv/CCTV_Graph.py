import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import platform

font = 'C:/Windows/Fonts/malgun.ttf'
font_name = font_manager.FontProperties(fname=font).get_name()
font_name
rc('font', family=font_name)

import pandas as pd
data_result = pd.read_csv('./data_result.csv', encoding='utf-8')
data_result.head()

data_result['CCTV비율'] = data_result['소계'] / data_result['인구수'] * 100
data_result['CCTV비율'].sort_values().plot(
        kind = 'barh',
        grid = True,
        figsize = (10,10)
    )
plt.show() # 가로막대

plt.figure(figsize = (6,6))
plt.scatter(data_result['인구수'], data_result['소계'], s=50)
plt.xlabel('인구수')
plt.ylabel('CCTV')
plt.grid()
plt.show() # 산점도

import numpy as np

fp1 = np.polyfit(
        data_result['인구수'],
        data_result['소계'],
        1
    )  # 직선구하기 명령
fp1
fy = np.poly1d(fp1) # y축데이터 숫자 1 조심
fx = np.linspace(100000, 700000, 100) # 인구수 범위

plt.figure(figsize=(10,10))
plt.scatter(data_result['인구수'], data_result['소계'], s=50)
plt.plot(fx, fy(fx), ls='dashed', lw=3, color='g')
plt.xlabel('인구수')
plt.ylabel('CCTV')
plt.grid()
plt.show() # 산점도

# 이 데이터에서 직선이 전체 데이터의 대표값을 의미한다면,
# 인구수가 4십만일때는 CCTV 는 1500 정도일 것이다.
# 이 기준값을 두고 오차를 계산할 수 있는 코드를 만들고, 오차가
# 큰 순으로 데이터를 정렬한다.

data_result['오차'] = np.abs(data_result['소계'] - fy(data_result['인구수']))
df_sort = data_result.sort_values(by='오차', ascending=False)
# 오차를 계산할 수 있는 코드를 생성한 후 오차가 큰 순으로 데이터 정렬
df_sort

plt.figure(figsize=(14,10))
plt.scatter(data_result['인구수'], data_result['소계'],
               c=data_result['오차'], s=50)
plt.plot(fx, fy(fx), ls='dashed', lw=3, color='g')

# 정규분포표에 따른 95% 신뢰도 구축을 위한 오차 0.025 * 2 
for i in range(10):
    plt.text(df_sort['인구수'][i] * 1.02,
            df_sort['소계'][i] * 0.098,
            df_sort.index[i],
            fontsize = 15)

plt.xlabel('인구수')
plt.ylabel('인구당비율')
plt.grid()
plt.show() # 산점도
