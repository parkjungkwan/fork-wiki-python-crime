import json
import folium
import pandas as pd

ctx = './data/'
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
police['범죄']
police['구별']
map_data =tuple(zip(police['구별'],police['범죄']))
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
