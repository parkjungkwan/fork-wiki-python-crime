import pandas as pd
import folium

ctx = '../data/'
state_geo = ctx+ 'us-states.json'
state_unemployment = ctx+'US_Unemployment_Oct2012.csv'
state_data = pd.read_csv(state_unemployment)
m = folium.Map(location=[37, -102], zoom_start=5)
m.choropleth(
    geo_data=state_geo,
    name='choropleth',
    data=state_data,
    columns=['State', 'Unemployment'],
    key_on='feature.id',
    fill_color='YlGn',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Unemployment Rate (%)'
)
folium.LayerControl().add_to(m)
m.save(ctx+'#292_folium_chloropleth_USA1.html')

