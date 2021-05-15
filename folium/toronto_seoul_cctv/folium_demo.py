import pandas as pd
import folium

state_geo = './us-states.json'
state_data = pd.read_csv('./US_Unemployment_Oct2012.csv')

m = folium.Map(location=[37,-102], zoom_start=5)

m.choropleth(
    geo_data = state_geo,
    name = 'choropleth',
    data = state_data,
    columns = ['State','Unemployment'],
    key_on = 'feature.id',
    fill_color = 'YlGn',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name = 'Unemployment Rate(%)'
    )
folium.LayerControl().add_to(m)
m.save('./USA_MAP.html')

