import pandas as pd
import numpy as np
import googlemaps
from sklearn import preprocessing
import matplotlib.pyplot as plt
import seaborn as sns
import folium

ctx = './data/'
crime_anal_police = pd.read_csv(ctx+'crime_in_Seoul.csv',thousands=',',encoding='euc-kr')
crime_anal_police.head()

gmaps_key = "AIzaSyD9d1pZQ-vrq-Gx1kWc1t-zcgP21S2zaso"
gmaps = googlemaps.Client(key = gmaps_key)
gmaps.geocode('서울중부경찰서', language='ko')
"""
[{'address_components': [{'long_name': '２７', 'short_name': '２７', 'types': ['premise']}, {'long_name': '수표로', 'short_name': '수표로', 'types': ['political', 'sublocality', 'sublocality_level_4']}, {'long_name': '을지로동', 'short_name': '을지로동', 'types': ['political', 'sublocality', 'sublocality_level_2']}, {'long_name': '중구', 'short_name': '중구', 'types': ['political', 'sublocality', 'sublocality_level_1']}, {'long_name': '서울특별시', 'short_name': '서울특별시', 'types': ['administrative_area_level_1', 'political']}, {'long_name': '대한민국', 'short_name': 'KR', 'types': ['country', 'political']}, {'long_name': '100-032', 'short_name': '100-032', 'types': ['postal_code']}], 'formatted_address': '대한민국 서울특별시 중구 을지로동 수표로 27', 'geometry': {'location': {'lat': 37.5636465, 'lng': 126.9895796}, 'location_type': 'ROOFTOP', 'viewport': {'northeast': {'lat': 37.56499548029149, 'lng': 126.9909285802915}, 'southwest': {'lat': 37.56229751970849, 'lng': 126.9882306197085}}}, 'place_id': 'ChIJc-9q5uSifDURLhQmr5wkXmc', 'plus_code': {'compound_code': 'HX7Q+FR 대한민국 서울특별시', 'global_code': '8Q98HX7Q+FR'}, 'types': ['establishment', 'point_of_interest', 'police']}]
"""

station_name = []

for name in crime_anal_police['관서명']:
    station_name.append('서울'+str(name[:-1])+'경찰서') # -1 전부
station_name

station_address = []
station_lat = [] # 위도
station_lng = [] # 경도
for name in station_name:
    tmp = gmaps.geocode(name, language='ko')
    station_address.append(tmp[0].get('formatted_address'))

    tmp_loc = tmp[0].get('geometry')
    station_lat.append(tmp_loc['location']['lat'])
    station_lng.append(tmp_loc['location']['lng'])
    print(name + '------->'+tmp[0].get('formatted_address'))
station_lat
station_lng

gu_name = []

for name in station_address:
    tmp = name.split()
    tmp_gu = [gu for gu in tmp if gu[-1] == '구'][0]
    print('***'+tmp_gu)
    gu_name.append(tmp_gu)
gu_name

type(crime_anal_police) # <class 'pandas.core.frame.DataFrame'>
len(crime_anal_police['관서명']) # 서울시내에 총 31개의 관할서가 존재함
crime_anal_police['구별'] = gu_name

crime_anal_police.head()

# 금천경찰서는 관악구 위치에 있어서 금천서는 제외
crime_anal_police[crime_anal_police['관서명']=='금천서']
crime_anal_police
crime_anal_police.loc[crime_anal_police['관서명']=='금천서',['구별']] = '금천구'
# 금천서를 찾아서 관악구로 되어있는 것을 금천구로 고쳐라

crime_anal_police.to_csv('./crime_in_Seoul_include_gu_name.csv', sep=',', encoding='utf-8')

# crime2 부분

import pandas as pd
import numpy as np
import googlemaps
from sklearn import preprocessing
import matplotlib.pyplot as plt
import seaborn as sns
import folium

crime_anal_police = pd.read_csv(ctx+'crime_in_Seoul_include_gu_name.csv',sep=',',encoding='utf-8')
crime_anal_police.head()

# ************
# Pivot_table 이용해서 데이터 정리하기
# ************

crime_anal_raw = pd.read_csv(ctx+'crime_in_Seoul_include_gu_name.csv',
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
data_result = pd.read_csv(ctx+'data_result.csv', encoding='utf-8',
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

# police_norm.to_csv('./crime_in_seoul_final.csv',sep=',',encoding='UTF-8')



police = police_norm

# crime3 부분

import json
import folium
import pandas as pd


police = pd.read_csv(ctx+'crime_in_seoul_final.csv', encoding='utf-8')
police.head()

# 서울시 토너맵으로 출력
geo_path = ctx+'geo_simple.json'
geo_path
geo_str = json.load(open(geo_path, encoding='UTF-8'))

map = folium.Map(location=[37.5502,126.982], 
                        zoom_start=12,
                        tiles='Stamen Toner')
map.save('./html/toner.html')

# 범죄발생건수를 토너맵으로 출력
police.head()
police.columns
map_data = police['범죄']
map_data
map = folium.Map(location=[37.5502,126.982], 
                        zoom_start=12,
                        tiles='Stamen Toner')
map.choropleth(
    geo_data = geo_str,
    data = map_data,
    columns = [police.index, police['범죄']],
    key_on = 'feature.id',
    fill_color = 'PuRd'
    )
map.save('./html/toner2.html')

# 경찰서 지도

police_position = pd.read_csv(ctx+'police_position.csv')

col = ['살인 검거','강도 검거','강간 검거','절도 검거','폭력 검거']
tmp = police_position[col] / police_position[col].max()
police_position['검거'] = np.sum(tmp, axis = 1)
# 각각의 범죄 검거를 검거라는 컬럼으로 합침

police_position.head()

police_position['lat'] = station_lat
police_position['lng'] = station_lng
map = folium.Map(location=[37.5502,126.982], 
                        zoom_start=12)
for i in police_position.index:
    folium.CircleMarker([police_position['lat'][i],
        police_position['lng'][i]],
                        radius = police_position['검거'][i] * 10,
                        color = '#31868cc',
                        fill_color = '#31868cc').add_to(map)
map.save('./html/police_position.html')

# 경찰서 위치 + 범죄율 지도

arr = police_position

map = folium.Map(location=[37.5502,126.982], 
                        zoom_start=12)
map_data = police['범죄']
map.choropleth(
    geo_data = geo_str,
    data = map_data,
    columns = [police.index, police['범죄']],
    key_on = 'feature.id',
    fill_color = 'PuRd'
    )
for i in arr.index:
    folium.CircleMarker([arr['lat'][i],arr['lng'][i]],
                        radius = arr['검거'][i] * 10,
                        color = '#31868cc',
                        fill_color = '#31868cc').add_to(map)
map.save('./html/result.html')