import pandas as pd
import numpy as np
import googlemaps
from sklearn import preprocessing
import matplotlib.pyplot as plt
import seaborn as sns
import folium
ctx = './data'
crime_anal_police = pd.read_csv(ctx+'crime_in_Seoul_include_gu_name.csv',sep=',',encoding='utf-8')
crime_anal_police.head()

# ************
# Pivot_table 이용해서 데이터 정리하기
# ************

crime_anal_raw = pd.read_csv('./crime_in_Seoul_include_gu_name.csv',
                                        encoding='utf-8')

crime_anal = pd.pivot_table(crime_anal_raw,
                            index='구별', aggfunc= np.sum) 
"""
aggfunc 은 numpy 의 평균값을 리턴하는 함수
"""
crime_anal.head() 
# 첫번째 컬럼이 구별로 전환됨
police = crime_anal
police['강간검거율'] = police['강간 검거'] / police['강간 발생'] * 100
police['강도검거율'] = police['강도 검거'] / police['강도 발생'] * 100
police['살인검거율'] = police['살인 검거'] / police['살인 발생'] * 100
police['절도검거율'] = police['절도 검거'] / police['절도 발생'] * 100
police['폭력검거율'] = police['폭력 검거'] / police['폭력 발생'] * 100

del police['강간 검거']
del police['강도 검거']
del police['살인 검거']
del police['절도 검거']
del police['폭력 검거']

con_list = ['강간검거율','강도검거율','살인검거율','절도검거율','폭력검거율']
con_list
for i in con_list:
    police.loc[police[i] > 100, i] = 100
police
# 검거율이 100이 넘는 값이 가끔 나옴.
# 1년 이상의 기간이 포함된 데이터 오류
# 비율이 100이 넘을 수 없으니 100 오버는 그냥 100으로 처리

police.rename(columns = {'강간 발생' : '강간',
                         '강도 발생' : '강도',
                         '살인 발생' : '살인',
                         '절도 발생' : '절도',
                         '폭력 발생' : '폭력'
                         }, inplace=True)

# 숫자값으로 모델링화 
col = ['강간','강도','살인','절도','폭력']
x = police[col].values
min_max_scalar = preprocessing.MinMaxScaler()
"""
스케일링은 자료 집합에 적용되는 전처리과정으로 모든 자료에
선형 변환을 적용하여 전체 자료의 분포를 
평균 0, 분산 1이 되도록 만드는 과정이다.
"""
x_scaled = min_max_scalar.fit_transform(x.astype(float))
#min_max_scalar(x) 는 최대/최소값이 각각 1, 0 이 되도록 스켈일링
police_norm = pd.DataFrame(x_scaled, columns=col, index=police.index)
# 각 컬럼별로 정규화 하기
col2 = ['강간검거율','강도검거율','살인검거율','절도검거율','폭력검거율']
police_norm[col2] = police[col2]

police_norm # 발생건수를 정규화시킴

# **********
# Crime 과 CCTV를 Merge 함
# **********
data_result = pd.read_csv('./data_result.csv', encoding='utf-8',
                          index_col='구별')
data_result.head()

police_norm[['인구수','CCTV']] = data_result[['인구수','소계']]
police_norm['범죄'] = np.sum(police_norm[col], axis=1)
police_norm['검거'] = np.sum(police_norm[col2], axis=1)


police_norm.head()
police_norm.columns

from matplotlib import font_manager, rc
font = 'C:/Windows/Fonts/malgun.ttf'
font_name = font_manager.FontProperties(fname=font).get_name()
font_name
rc('font', family=font_name)

sns.pairplot(
    police_norm,
    vars = ["강도","살인","폭력"],
    kind = 'reg',  # regression 선형회귀
    height = 3
    )

plt.show()
# 강도와 폭력, 살인과 폭력, 강도와 살인은 모두
# 양의 상관관계를 갖는다
sns.pairplot(
    police_norm,
    x_vars = ["인구수","CCTV"],
    y_vars = ["살인","강도"],
    kind = 'reg',  # regression 선형회귀
    height = 3
    )

plt.show()

# 인구수와 CCTV 갯수, 그리고 살인과 강도사건
# 전체적인 상관계수는 CCTV와 살인의 관계가
# 낮을지 몰라도(방지효과)
# CCTV 가 없을 때 살인이 많이 일어나는 구간이
# 있습니다. 즉 CCTV 갯수를 기준으로 좌측면에
# 살인과 강도의 높은 수를 갖는 데이터가 보입니다.

sns.pairplot(
    police_norm,
    x_vars = ["인구수","CCTV"],
    y_vars = ["살인검거율","폭력검거율"],
    kind = 'reg',  # regression 선형회귀
    height = 3
    )

plt.show()
# 그러나, 검거율과 CCTV의 관계가 양의상관관계가 아닙니다.
# 오히려 음의 상관관계도 보입니다.
# 또, 인구수와 검거율도 음의 상관관계가 보입니다.

tmp_max = police_norm['검거'].max()
police_norm['검거'] = police_norm['검거'] / tmp_max * 100
police_norm_sort = police_norm.sort_values(by='검거', ascending=False)
police_norm_sort.head()
target_col = col2
police_norm_sort = police_norm.sort_values(by='검거', ascending=False)
plt.figure(figsize = (10,10))

sns.heatmap(police_norm_sort[target_col], annot=True,fmt='f', linewidths=5)
plt.title("범죄 검거 비율(정규화된 검거의 합으로 정렬)")
plt.show()

# 발생건수의 합으로 정렬해서  heatmap 으로 관찰
target_col = ['강간','강도','살인','절도','폭력',"범죄"] # 범죄추가

police_norm["범죄"] = police_norm["범죄"] /5
police_norm_sort = police_norm.sort_values(by='검거', ascending=False)
plt.figure(figsize = (10,10))

sns.heatmap(police_norm_sort[target_col], annot=True,fmt='f', linewidths=5)
plt.title("범죄 비율(정규화된 검거의 합으로 정렬)")
plt.show()

# 발생건수의 합으로 정렬해서  heatmap 으로 관찰
# 강남구, 양천구, 영등포구 가 범죄발생건수가 높습니다.
# 송파구와 서초구도 낮다고 볼수 없습니다.
# 정말 강남 3구가 안전한가에 대한 의문이 생김

police_norm.to_csv('./crime_in_seoul_final.csv',sep=',',encoding='UTF-8')

police_norm.columns
