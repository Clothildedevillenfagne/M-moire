#!/usr/bin/env python
# coding: utf-8

# # Animal evolution in Belgium

# #### <br> Visualize the data base


# In[]:
import pandas as pd
import warnings
import requests
import zipfile
import io
import geopandas as gpd
from tkinter import *
import folium
import numpy as np
from folium.plugins import MarkerCluster
import webbrowser
import os
from shapely.geometry import Polygon, Point, MultiPolygon
from shapely.geometry import shape
import json

warnings.filterwarnings("ignore")

# In[]:
df = pd.read_csv(r'/Users/clothildedevillenfagne/Cours/Master_2/Mémoire/moyen_data.csv', sep="\t")

# In[]:
url_prov = "https://www.odwb.be/explore/dataset/provincesprovincies-belgium/download/?format=shp&timezone=Europe/Brussels&lang=fr"
local_path = "tmp/"  # folder to create
filter_prov = []  # only metropolitan France

r = requests.get(url_prov)
z = zipfile.ZipFile(io.BytesIO(r.content))
z.extractall(path=local_path)
filenames = [
    y
    for y in sorted(z.namelist())
    for ending in ["dbf", "prj", "shp", "shx"]
    if y.endswith(ending)
]
dbf, prj, shp, shx = [filename for filename in filenames]
fr = gpd.read_file(local_path + shp)  # + encoding="utf-8" if needed
fr.crs = "epsg:4326"  # {'init': 'epsg:4326'}
met = fr.query("prov_code not in @filter_prov")
met.set_index("prov_code", inplace=True)
met = met["geometry"]
prov_code = list(fr["prov_code"])



# In[]:
liste_com = []
geo = []
fd = open("communesgemeente-belgium.geojson", "r")
if fd :
    data = json.load(fd)
    for i in range(len(data["features"])):
        #try:
        liste_com.append(data["features"][i]["properties"]["arr_code"])
        #except:
        #    liste_com.append(data["features"][i]["properties"]["arr_name_nl"])

        geom = shape(data["features"][i]["geometry"])
        #print(type(geom))
        geo.append(geom)
df_geo = pd.DataFrame({'commune': liste_com, 'geometry': geo})

# In[1]:

''' Ce programme peut seulement faire une carte avec les donner fournie par natagora et NatuurPunt
    Makes a HTML document in the same directory as this script 
'''
provList = ["West Flanders", "Flemish Brabant", "East Flanders", "Namur", "Liège", "Hainaut",
            "Luxembourg", "Walloon Brabant", "Limburg", "Antwerp", "Brussels Capital Region"]

basemaps = ["OpenStreetMap", "MapQuest Open", "MapQuest Open Aerial",
            "Mapbox Bright", "Mapbox Control Room", "CartoDB dark_matter",
            "CartoDB positron", "Stamen Terrain", "Stamen Toner",
            "Stamen Watercolor"]

colors = ['red', 'blue', 'gray', 'darkred', 'lightred', 'orange', 'beige', 'green', 'darkgreen',
          'lightgreen', 'darkblue', 'lightblue', 'purple', 'darkpurple', 'pink', 'cadetblue',
          'lightgray', 'black']

master = Tk()

master.title("Outil de visualisation")

# Label(master, text="Choisissez une carte").grid(row=0)
Label(master, text="Nom de l'espèce").grid(row=0)
Label(master, text="Seul le nom sientifique des espèce est attendu").grid(row=0, column=2)
Label(master, text="Province").grid(row=2)
Label(master, text="Année").grid(row=3)
Label(master, text="à").grid(row=3, column=2)
Label(master, text="Avec groupement ?").grid(row=4)
Label(master, text="Nom de la carte enregistée").grid(row=5)

# e1 = Entry(master)
userespece = Entry(master)

# e1.grid(row=0, column=1)
userespece.grid(row=0, column=1)

userAnnee1 = Entry(master)
userAnnee1.grid(row=3, column=1)

userAnnee2 = Entry(master)
userAnnee2.grid(row=3, column=3)

cb = IntVar()
Checkbutton(master, variable=cb, onvalue=1, offvalue=0).grid(row=4, column=1)

nomFichier = Entry(master)
nomFichier.grid(row=5, column=1)

var2 = StringVar(master)
var2.set(provList[0])  # initial value

option2 = OptionMenu(master, var2, *provList)
option2.grid(row=2, column=1)


def makeMap(df, espece, code_prov, annee1, annee2, groupe, fichier):
    df = df[df.species == str(espece)]  # select the species
    min = df['year'] >= int(annee1)
    df_min = df[min]
    max = df_min['year'] <= int(annee2)
    df_final = df_min[max]

    for i in range(len(prov_code)):
        if prov_code[i] == code_prov:
            p = met[i]
            center = p.centroid
            loc = np.array(center)
            break
        else:
            loc = [4.35, 50.8333]

    gdf = gpd.GeoDataFrame(
        df_final, geometry=gpd.points_from_xy(df_final.decimalLongitude, df_final.decimalLatitude))

    # associer commune a chaque coordoné
    com = []
    for pt in gdf['geometry']:
        count = 0
        for zone in df_geo.itertuples():
            if zone.geometry.contains(pt):
                com.append(zone.commune)
                break
            if count == len(df_geo) - 1:
                com.append('NaN')
            count += 1
    df_final['commune']=com
    latitude = df_final['decimalLatitude'].tolist()
    longitude = df_final['decimalLongitude'].tolist()
    individualCount = df_final['individualCount'].tolist()
    year = df_final['year'].tolist()

    mappy = folium.Map(location=[loc[1], loc[0]], zoom_start=20)  # tiles=basemap,

    mappy.choropleth(geo_data="communesgemeente-belgium.geojson",
                   # I found this NYC zipcode boundaries by googling
                   data=df_final,  # my dataset
                   columns=['commune', 'individualCount'],
                   # zip code is here for matching the geojson zipcode, sales price is the column that changes the color of zipcode areas
                   key_on='feature.properties.arr_code',
                   # this path contains zipcodes in str type, this zipcodes should match with our ZIP CODE column
                   fill_color='BuPu', fill_opacity=0.7, line_opacity=0.3,
                   legend_name='Nombre d''individus apperçu')

    folium.TileLayer('openstreetmap').add_to(mappy)
    folium.TileLayer('Stamen Terrain').add_to(mappy)
    folium.TileLayer('Stamen Toner').add_to(mappy)
    folium.TileLayer('Stamen Watercolor').add_to(mappy)
    folium.TileLayer('CartoDB positron').add_to(mappy)
    folium.TileLayer('CartoDB dark_matter').add_to(mappy)

    if groupe == 1:

        marker_cluster = MarkerCluster().add_to(mappy)

        for i in range(len(latitude)):
            folium.Marker([latitude[i], longitude[i]], popup="""
                  <i>Nombre d'individue compté: </i><b><br>{}</b><br>
                  <i>Année de l'observation: </i><b><br>{}</b><br>""".format(
                round(individualCount[i], 2),
                round(year[i], 2))).add_to(marker_cluster)


    else:
        for i in range(len(latitude)):
            folium.Marker([latitude[i], longitude[i]], popup="""
                  <i>Nombre d'individue compté: </i><b><br>{}</b><br>
                  <i>Année de l'observation: </i><b><br>{}</b><br>""".format(
                round(individualCount[i], 2),
                round(year[i], 2))).add_to(mappy)

    folium.LayerControl().add_to(mappy)
    mappy.save(fichier + '.html')
    filename = 'file:///' + os.getcwd() + '/' + fichier + '.html'
    webbrowser.open(filename)  # open_new_tab


def ok():
    # print("Basemap: ", var1.get())
    print("Espèce: ", userespece.get())
    print("Province: ", var2.get())
    print("Année de début: ", userAnnee1.get())
    print("Année de fin: ", userAnnee2.get())
    print("Nom de la carte: ", nomFichier.get())
    if cb.get() == 1:
        print("Demande de groupement : OUI")
    else:
        print("Demande de groupement : NON")
    # base = var1.get()
    espece = userespece.get()
    province = var2.get()
    annee1 = userAnnee1.get()
    annee2 = userAnnee2.get()
    groupe = cb.get()
    fichier = nomFichier.get()
    new_df = df[['species', 'individualCount', 'year', 'decimalLatitude', 'decimalLongitude']].copy()
    if province == "West Flanders":
        code = "30000"
    elif province == "Flemish Brabant":
        code = "20001"
    elif province == "East Flanders":
        code = "40000"
    elif province == "Namur":
        code = "90000"
    elif province == "Liège":
        code = "60000"
    elif province == "Hainaut":
        code = "50000"
    elif province == "Luxembourg":
        code = "80000"
    elif province == "Walloon Brabant":
        code = "20002"
    elif province == "Limburg":
        code = "70000"
    elif province == "Antwerp":
        code = "10000"
    else:
        code = "00000"
    makeMap(new_df, espece, code, annee1, annee2, groupe, fichier)


button = Button(master, text="OK", command=ok)
button.grid(row=6, column=0)

master.mainloop()

# Delichon urbicum
