import  pandas as pd
import googlemaps

ctx = '../data/'
filename = 'crime_in_Seoul.csv'
df_crime = pd.read_csv(ctx+filename,
                       thousands=',',
                       encoding='euc-kr')
gmaps_key = 'AIzaSyD9d1pZQ-vrq-Gx1kWc1t-zcgP21S2zaso'
gmaps = googlemaps.Client(key=gmaps_key)


"""
['관서명', '살인
 
 발생', '살인 검거', '강도 발생',
 '강도 검거', '강간 발생', '강간 검거', '절도 발생',
       '절도 검거', '폭력 발생', '폭력 검거']
"""
# print(gmaps.geocode('서울중부경찰서', language='ko'))

station_name = []

for name in df_crime['관서명']:
    station_name.append('서울'+str(name[:-1])+'경찰서')

station_addr = []
station_lat = [] #위도
station_lng = [] #경도

for name in station_name:
    tmp = gmaps.geocode(name, language='ko')
    station_addr.append(tmp[0].get('formatted_address'))
    tmp_loc = tmp[0].get('geometry')
    station_lat.append(tmp_loc['location']['lat'])
    station_lng.append(tmp_loc['location']['lng'])
    # print(name + '--------->'+tmp[0].get('formatted_address'))

gu_names = []
for name in station_addr:
    tmp = name.split()
    tmp_gu = [gu for gu in tmp if gu[-1] == '구'][0]
    gu_names.append(tmp_gu)
print('------ 1 -----')
print(len(df_crime['관서명']))

df_crime['구별'] = gu_names
print('------ 2 -----')
print(df_crime['관서명'])

# 금천경찰서는 관악구에 있어서
print('------ 3 -----')
# 금천서를 찾아서 관악구라고 수동으로 작업해야 함

df_crime.loc[df_crime['관서명'] == '금천서',['구별']] == '금천구'
print(df_crime)

df_crime.to_csv(ctx+'crime_police.csv')





















