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
from folium import FeatureGroup
import numpy as np
from folium.plugins import MarkerCluster
import webbrowser
import os

warnings.filterwarnings("ignore")

# In[]:
df = pd.read_csv(
    r'/Users/clothildedevillenfagne/Cours/Master_2/Mémoire/data_reduite_obs.csv')  # moyen_data.csv, sep="\t"

# In[]:
df

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

green_bleu = ['lightgreen', 'green', 'darkgreen', 'lightblue', 'cadetblue', 'blue', 'darkblue', 'lightgray', 'gray',
              'black']

purple_red = ['beige', 'orange', 'purple', 'darkpurple', 'pink', 'lightred', 'red', 'darkred']

bleu = ['#191970', '#000080', '#00008B', '#0000CD', '#0000FF', '#00FFFF', '#00FFFF', '#E0FFFF', '#AFEEEE', '#7FFFD4',
        '#40E0D0', '#48D1CC', '#00CED1', '#5F9EA0', '#4682B4', '#B0C4DE', '#B0E0E6', '#ADD8E6', '#87CEEB', '#87CEFA',
        '#00BFFF', '#1E90FF', '#6495ED', '#7B68EE', '#4169E1']

master = Tk()

master.title("Outil de visualisation")

# Label(master, text="Choisissez une carte").grid(row=0)
Label(master, text="Nom de l'espèce").grid(row=0)
Label(master, text="Seul le nom sientifique des espèce est attendu").grid(row=0, column=2)
# Label(master, text="Province").grid(row=2)
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


def makeMap(df, espece, annee1, annee2, groupe, fichier):  # code_prov,
    df = df[df.species == str(espece)]  # select the species
    min = df['year'] >= int(annee1)
    df_min = df[min]
    max = df_min['year'] <= int(annee2)
    df_final = df_min[max]

    '''for i in range(len(prov_code)):
        if prov_code[i] == code_prov:
            p = met[i]
            center = p.centroid
            loc = np.array(center)
            break
        else:
            loc = [4.35, 50.8333]'''

    loc = [4.35, 50.8333]

    mappy = folium.Map(location=[loc[1], loc[0]], zoom_start=10)  # tiles=basemap,

    folium.TileLayer('openstreetmap').add_to(mappy)
    folium.TileLayer('Stamen Terrain').add_to(mappy)
    folium.TileLayer('Stamen Toner').add_to(mappy)
    folium.TileLayer('Stamen Watercolor').add_to(mappy)
    folium.TileLayer('CartoDB positron').add_to(mappy)
    folium.TileLayer('CartoDB dark_matter').add_to(mappy)

    longitude = df_final['decimalLongitude'].tolist()
    latitude = df_final['decimalLatitude'].tolist()
    individualCount = df_final['individualCount'].tolist()
    year = df_final['year'].tolist()
    num_obs = df_final['numberObservation'].tolist()

    if groupe == 1:

        marker_cluster = MarkerCluster().add_to(mappy)

        for i in range(len(latitude)):
            if int(annee2) - int(annee1) == 0:
                col = 'blue'
            else:
                dif = (year[i] - int(annee1)) % len(green_bleu)
                col = green_bleu[dif]
            folium.Marker([latitude[i], longitude[i]], popup="""
                  <i>Nombre d'individue compté: </i><b><br>{}</b><br>
                  <i>Année de l'observation: </i><b><br>{}</b><br>""".format(
                round(individualCount[i], 2),
                round(year[i], 2)), icon=folium.Icon(color=col, icon='fa-circle', prefix='fa')).add_to(marker_cluster)


    else:

        annee = int(annee1)
        lgd_txt = '<span style="color: {col};">{txt}</span>'
        dico_feature = {}
        while annee <= int(annee2):
            dif = (annee - int(annee1)) % len(green_bleu)
            col = green_bleu[dif]
            dico_feature[annee] = FeatureGroup(name=lgd_txt.format(txt=annee, col=col))
            dico_feature[annee].add_to(mappy)
            annee += 1

        for i in range(len(latitude)):
            if int(annee2) - int(annee1) == 0:
                col = 'blue'
            else:
                dif = (year[i] - int(annee1)) % len(green_bleu)
                col = green_bleu[dif]

            folium.CircleMarker(location=(latitude[i], longitude[i]), radius=num_obs[i],
                                popup="""
                                 <i>Nombre d'individue compté: </i><b><br>{}</b><br>
                                 <i>Année de l'observation: </i><b><br>{}</b><br>""".format(
                                    round(individualCount[i], 2),
                                    round(year[i], 2)),  # line_color=col,
                                color=col, fill=False).add_to(dico_feature[year[i]])  # '#3186cc'
            '''folium.Marker([latitude[i], longitude[i]], popup="""
                  <i>Nombre d'individue compté: </i><b><br>{}</b><br>
                  <i>Année de l'observation: </i><b><br>{}</b><br>""".format(
                round(individualCount[i], 2),
                round(year[i], 2)), icon=folium.Icon(color=col, icon='fa-circle', prefix='fa')).add_to(mappy) '''  # , icon=folium.Icon(color=col,icon_color=col)
        annee = int(annee1)
        while annee > int(annee2):
            #dico_feature[annee].add_to(mappy)
            mappy.add_child(dico_feature[annee])
            annee += 1
        #mappy.add_child(folium.map.LayerControl())

    folium.LayerControl().add_to(mappy)
    # lien = fichier + '.html'
    url = 'https://docs.python.org/'
    mappy.save(fichier + '.html')
    filename = 'file:///' + os.getcwd() + '/' + fichier + '.html'
    # webbrowser.open(fichier + '.html')
    webbrowser.open(filename)  # open_new_tab


def ok():
    # print("Basemap: ", var1.get())
    print("Espèce: ", userespece.get())
    # print("Province: ", var2.get())
    print("Année de début: ", userAnnee1.get())
    print("Année de fin: ", userAnnee2.get())
    print("Nom de la carte: ", nomFichier.get())
    if cb.get() == 1:
        print("Demande de groupement : OUI")
    else:
        print("Demande de groupement : NON")
    # base = var1.get()
    espece = userespece.get()
    # province = var2.get()
    annee1 = userAnnee1.get()
    annee2 = userAnnee2.get()
    groupe = cb.get()
    fichier = nomFichier.get()
    new_df = df[
        ['species', 'individualCount', 'year', 'decimalLatitude', 'decimalLongitude', 'numberObservation']].copy()
    '''if province == "West Flanders":
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
        code = "00000"'''
    # makeMap(new_df, espece, code, annee1, annee2, groupe, fichier)
    makeMap(new_df, espece, annee1, annee2, groupe, fichier)


button = Button(master, text="OK", command=ok)
button.grid(row=6, column=0)

master.mainloop()

# Delichon urbicum
