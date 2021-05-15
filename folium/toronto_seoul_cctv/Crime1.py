import pandas as pd
import numpy as np
import googlemaps
from sklearn import preprocessing
import matplotlib.pyplot as plt
import seaborn as sns
import folium

crime_anal_police = pd.read_csv('./crime_in_Seoul.csv',thousands=',',encoding='euc-kr')
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
