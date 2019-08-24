import pandas as pd
import folium

class FoliumTest:
    def __init__(self):
        self.context = './data'

    def hook(self):
        self.show_map()

    def show_map(self):
        state_geo = self.context + '/us-states.json'
        state_unemployment = self.context+'/us_unemployment.csv'
        state_data = pd.read_csv(state_unemployment)
        m = folium.Map(location=[37,-102], zoom_start=5)
        m.choropleth(
            geo_data = state_geo,
            name = 'choropleth',
            data = state_data,
            columns = ['State', 'Unemployment'],
            key_on = 'feature.id',
            fill_color = 'YlGn',
            fill_opacity = 0.7,
            line_opacity = 0.2,
            legend_name = 'Unemployment Rate (%)'
        )
        folium.LayerControl().add_to(m)
        m.save('./saved_data/USA.html')
