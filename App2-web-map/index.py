# folium is library for Map
import folium
import pandas
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
df = pandas.read_csv(dir_path+"/Volcanoes.txt")

lat = list(df["LAT"])
lon = list(df["LON"])
elev = list(df["ELEV"])
name = list(df["NAME"])

def color_elev(elev) :
    if elev < 1000:
        return "green"
    elif 1000 <= elev <3000 :
        return "orange"
    else :
        return "red"

html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

map = folium.Map(location=[38.58, -99.09], zoom_start=6, tiles = "Stamen Terrain")

## ADD LAYER WITH VOCALNOES
# add Marker to map
fgv = folium.FeatureGroup(name="Volcanoes")
coordinates = zip(lat,lon,elev,name)
for lt, ln, elv, nam in coordinates:
    #show popup as html
    iframe = folium.IFrame(html=html % (nam, nam, elv), width=200, height=100)
    #add marker
    #fgv.add_child(folium.Marker(location=[lt, ln], popup=folium.Popup(iframe), icon=folium.Icon(color=color_elev(elv))))
    #add circle marker. opacity = transparent
    fgv.add_child(folium.CircleMarker(location=[lt, ln], radius= 6, popup=folium.Popup(iframe), fill_color=color_elev(elv), color="grey", fill_opacity = 0.7 ))

## ADD LAYER WITH COUNTRY AND POPULATION

# add third layer, add polygon for map. which is in world.json, which contain GPS of all places
fgp = folium.FeatureGroup(name="Population")
with open("world.json", 'r', encoding="utf-8-sig") as file :
    fgp.add_child(folium.GeoJson(data=file.read(),
    style_function= lambda x: {'fillColor':'green' if x['properties']['POP2005']< 10000000 else 'orange' if 10000000 <= x['properties']['POP2005'] <20000000 else 'red'}))

map.add_child(fgv)
map.add_child(fgp)

# Turn ON layer control
map.add_child(folium.LayerControl())

map.save("Map_advance.html")