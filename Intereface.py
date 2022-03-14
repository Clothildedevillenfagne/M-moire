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
df = pd.read_csv(r'./data_reduite_obs.csv')  # moyen_data.csv, sep="\t"

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

list_espece1 = sorted(set(df['species'].tolist()))

list_espece2 = ['Pas d\'autre espèce'] + list_espece1

list_kig = sorted(set(df['kingdom'].tolist()))

list_phy = sorted(set(df['phylum'].tolist()))
#list_phy = [x for x in list_phy if pd.isnull(x) == False]

list_class = set(df['class'].tolist())
list_class = [x for x in list_class if pd.isnull(x) == False]
list_class = sorted(list_class)

list_or = set(df['order'].tolist())
list_or = [x for x in list_or if pd.isnull(x) == False]
list_or = sorted(list_or)

list_fam = set(df['family'].tolist())
list_fam = [x for x in list_fam if pd.isnull(x) == False]
list_fam = sorted(list_fam)

list_ge = set(df['genus'].tolist())
list_ge = [x for x in list_ge if pd.isnull(x) == False]
list_ge = sorted(list_ge)

master = Tk()

master.title("Outil de visualisation")

# Label(master, text="Choisissez une carte").grid(row=0)
Label(master, text= "Précision de la taxonomie souhaité (seul le rang séléctionné sera pris en compte)").grid(row=0)
#Label(master, text="Nom de l'espèce").grid(row=2)
#Label(master, text="Nom de l'espèce 2").grid(row=3)
#Label(master, text="Seul le nom sientifique des espèce est attendu").grid(row=0, column=2)
# Label(master, text="Province").grid(row=2)
Label(master, text="Année").grid(row=4)
Label(master, text="à").grid(row=4, column=2)
Label(master, text="Avec groupement ?").grid(row=5)
Label(master, text="Nom de la carte enregistée").grid(row=6)


var = IntVar()

kig = Radiobutton(master, text="Règne", variable=var, value=7).grid(row=1, column=0)
phy = Radiobutton(master, text="Embranchement", variable=var, value=6).grid(row=1, column=1)
cl = Radiobutton(master, text="Classe", variable=var, value=5).grid(row=1, column=2)
ord = Radiobutton(master, text="Ordre", variable=var, value=4).grid(row=1, column=3)
fam = Radiobutton(master, text="Famille", variable=var, value=3).grid(row=1, column=4)
ge = Radiobutton(master, text="Genre", variable=var, value=2).grid(row=1, column=5)
esp = Radiobutton(master, text="Espèce", variable=var, value=1).grid(row=1, column=6)

varesp1 = StringVar(master)
varesp1.set(list_espece1[0])  # initial value
userespece = OptionMenu(master, varesp1, *list_espece1)
userespece.grid(row=2, column=6)

varesp2 = StringVar(master)
varesp2.set(list_espece2[0])
userespece2 = OptionMenu(master, varesp2, *list_espece2)
userespece2.grid(row=3, column=6)

varkig = StringVar(master)
varkig.set(list_kig[0])  # initial value
userkig = OptionMenu(master, varkig, *list_kig)
userkig.grid(row=2, column=0)

varphy = StringVar(master)
varphy.set(list_phy[0])
userphy = OptionMenu(master, varphy, *list_phy)
userphy.grid(row=2, column=1)

varclass = StringVar(master)
varclass.set(list_class[0])
userfam = OptionMenu(master, varclass, *list_class)
userfam.grid(row=2, column=2)

varor = StringVar(master)
varor.set(list_or[0])
useror = OptionMenu(master, varor, *list_or)
useror.grid(row=2, column=3)

varfam = StringVar(master)
varfam.set(list_fam[0])
userfam = OptionMenu(master, varfam, *list_fam)
userfam.grid(row=2, column=4)

varge = StringVar(master)
varge.set(list_ge[0])
userge = OptionMenu(master, varge, *list_ge)
userge.grid(row=2, column=5)


userAnnee1 = Entry(master)
userAnnee1.grid(row=4, column=1)

userAnnee2 = Entry(master)
userAnnee2.grid(row=4, column=3)

cb = IntVar()
Checkbutton(master, variable=cb, onvalue=1, offvalue=0).grid(row=5, column=1)

nomFichier = Entry(master)
nomFichier.grid(row=6, column=1)

def makeMapGroupement (df_final, map, espece,  annee1, annee2, color):

    longitude = df_final['decimalLongitude'].tolist()
    latitude = df_final['decimalLatitude'].tolist()
    individualCount = df_final['individualCount'].tolist()
    year = df_final['year'].tolist()

    annee = int(annee1)
    lgd_txt = '<span style="color: {col};">{txt}</span>'
    dico_feature = {}
    dico_cluster = {}
    while annee <= int(annee2):
        dif = (annee - int(annee1)) % len(color)
        col = color[dif]
        dico_feature[annee] = FeatureGroup(name=lgd_txt.format(txt= str(annee) + ' ' + espece, col=col))
        dico_cluster[annee] = MarkerCluster().add_to(dico_feature[annee])
        # dico_feature[annee].add_to(marker_cluster)
        dico_feature[annee].add_to(map)
        annee += 1

    for i in range(len(latitude)):
        if int(annee2) - int(annee1) == 0:
            col = 'blue'
        else:
            dif = (year[i] - int(annee1)) % len(color)
            col = color[dif]
        folium.Marker([latitude[i], longitude[i]], popup="""
                  <i>Nombre d'individue compté: </i><b><br>{}</b><br>
                  <i>Année de l'observation: </i><b><br>{}</b><br>""".format(
            round(individualCount[i], 2),
            round(year[i], 2)), icon=folium.Icon(color=col, icon='fa-circle', prefix='fa')).add_to(
            dico_cluster[year[i]])  # marker_cluster)
    annee = int(annee1)

    while annee > int(annee2):
        map.add_child(dico_feature[annee])
        annee += 1

    return map

def makeMapNonGroup(df_final, map, espece, annee1, annee2, color):
    longitude = df_final['decimalLongitude'].tolist()
    latitude = df_final['decimalLatitude'].tolist()
    individualCount = df_final['individualCount'].tolist()
    year = df_final['year'].tolist()
    num_obs = df_final['numberObservation'].tolist()

    annee = int(annee1)
    lgd_txt = '<span style="color: {col};">{txt}</span>'
    dico_feature = {}
    while annee <= int(annee2):
        dif = (annee - int(annee1)) % len(color)
        col = color[dif]
        dico_feature[annee] = FeatureGroup(name=lgd_txt.format(txt=str(annee)+' '+espece, col=col))
        dico_feature[annee].add_to(map)
        annee += 1

    for i in range(len(latitude)):
        if int(annee2) - int(annee1) == 0:
            col = 'blue'
        else:
            dif = (year[i] - int(annee1)) % len(color)
            col = color[dif]

        folium.CircleMarker(location=(latitude[i], longitude[i]), radius=np.log(num_obs[i]),
                            popup="""
                                     <i>Nombre d'individue compté: </i><b><br>{}</b><br>
                                     <i>Année de l'observation: </i><b><br>{}</b><br>
                                     <i>Nombre d'observation: </i><b><br>{}</b><br>""".format(
                                round(individualCount[i], 2),
                                round(year[i], 2),
                                round(num_obs[i], 2)),  # line_color=col,
                            color=col, fill=False).add_to(dico_feature[year[i]])  # '#3186cc'

    annee = int(annee1)
    while annee > int(annee2):
        # dico_feature[annee].add_to(mappy)
        map.add_child(dico_feature[annee])
        annee += 1

    return map




def makeMap(df,tax, espece1, espece2, annee1, annee2, groupe, fichier):  # code_prov,
    if tax == "species":
        df1 = df[df.species == str(espece1)].copy()  # select the species
        min = df1['year'] >= int(annee1)
        df_min = df1[min]
        max = df_min['year'] <= int(annee2)
        df_final1 = df_min[max]

        if espece2 != 'Pas d\'autre espèce':
            df2 = df[df.species == str(espece2)].copy()  # select the species
            min2 = df2['year'] >= int(annee1)
            df_min2 = df2[min2]
            max2 = df_min2['year'] <= int(annee2)
            df_final2 = df_min2[max2]

    else:
        df1 = df[df[tax] == str(espece1)].copy()
        min = df1['year'] >= int(annee1)
        df_min = df1[min]
        max = df_min['year'] <= int(annee2)
        df_final1 = df_min[max]
        year = []
        for i in range(int(annee1)-int(annee2)+1):
            year.append(int(annee1)+i)
        ar=[]
        for ye in year:
            new_df = df[df.year == ye].copy()
            longitude = set(new_df['decimalLongitude'].tolist())
            count = 0
            print('année :', ye)
            for lon in longitude:
                new_new_df = new_df[new_df.decimalLongitude == lon].copy()
                latitude = set(new_new_df['decimalLatitude'].tolist())
                for la in latitude:  # d'abord refaire un for pour longitude puis latitude
                    final_df = new_new_df[new_new_df.decimalLatitude == la].copy()
                    num_obs = final_df['numberObservation'].sum()
                    sums = final_df['individualCount'].sum()
                    new_line = [sums, la, lon, ye, num_obs]
                    ar.append(new_line)
            df_final1 = pd.DataFrame(ar, columns=['individualCount', 'decimalLatitude',
                                                'decimalLongitude', 'year', 'numberObservation'])

    loc = [4.35, 50.8333]

    mappy = folium.Map(location=[loc[1], loc[0]], zoom_start=10)  # tiles=basemap,

    folium.TileLayer('openstreetmap').add_to(mappy)
    folium.TileLayer('Stamen Terrain').add_to(mappy)
    folium.TileLayer('Stamen Toner').add_to(mappy)
    folium.TileLayer('Stamen Watercolor').add_to(mappy)
    folium.TileLayer('CartoDB positron').add_to(mappy)
    folium.TileLayer('CartoDB dark_matter').add_to(mappy)

    if groupe == 1:

        mappy = makeMapGroupement(df_final1,mappy, espece1, annee1, annee2, green_bleu)

        if espece2 != 'Pas d\'autre espèce':
            mappy = makeMapGroupement(df_final2, mappy, espece2, annee1, annee2, purple_red)


    else:

        mappy = makeMapNonGroup(df_final1, mappy, espece1, annee1, annee2, green_bleu)

        if espece2 != 'Pas d\'autre espèce':
            mappy = makeMapNonGroup(df_final2, mappy, espece2, annee1, annee2, purple_red)

    folium.LayerControl().add_to(mappy)
    mappy.save(fichier + '.html')
    filename = 'file:///' + os.getcwd() + '/' + fichier + '.html'
    webbrowser.open(filename)  # open_new_tab


def ok():
    variable = var.get()
    if variable == 1:
        tax = "species"
        print("Taxonomie souhaité: ", tax)
        print("Espèce 1: ", varesp1.get())
        print("Espèce 2: ", varesp2.get())
        espece1 = varesp1.get()
        espece2 = varesp2.get()

    elif variable == 2:
        tax = "genus"
        print("Taxonomie souhaité: ", tax)
        print("Genre: ", varge.get())
        espece1 = varge.get()
        espece2 = 'Pas d\'autre espèce'
    elif variable == 3:
        tax = "family"
        print("Taxonomie souhaité: ", tax)
        print("Famille: ", varfam.get())
        espece1 = varfam.get()
        espece2 = 'Pas d\'autre espèce'
    elif variable == 4:
        tax = "order"
        print("Taxonomie souhaité: ", tax)
        print("Ordre: ", varor.get())
        espece1 = varor.get()
        espece2 = 'Pas d\'autre espèce'
    elif variable == 5:
        tax = "class"
        print("Taxonomie souhaité: ", tax)
        print("Classe: ", varclass.get())
        espece1 = varclass.get()
        espece2 = 'Pas d\'autre espèce'
    elif variable == 6:
        tax = "phylum"
        print("Taxonomie souhaité: ", tax)
        print("Embranchement: ", varphy.get())
        espece1 = varphy.get()
        espece2 = 'Pas d\'autre espèce'
    else:
        tax = "kingdom"
        print("Taxonomie souhaité: ", tax)
        print("Règne: ", varkig.get())
        espece1 = varkig.get()
        espece2 = 'Pas d\'autre espèce'
    # print("Province: ", var2.get())
    print("Année de début: ", userAnnee1.get())
    print("Année de fin: ", userAnnee2.get())
    print("Nom de la carte: ", nomFichier.get())
    if cb.get() == 1:
        print("Demande de groupement : OUI")
    else:
        print("Demande de groupement : NON")
    # base = var1.get()

    # province = var2.get()
    annee1 = userAnnee1.get()
    annee2 = userAnnee2.get()
    groupe = cb.get()
    fichier = nomFichier.get()
    new_df = df[
        ['kingdom', 'phylum', 'class', 'order', 'family', 'genus','species', 'individualCount', 'year', 'decimalLatitude', 'decimalLongitude', 'numberObservation']].copy()

    makeMap(new_df,tax, espece1, espece2, annee1, annee2, groupe, fichier)


button = Button(master, text="OK", command=ok)
button.grid(row=7, column=0)

master.mainloop()

# Delichon urbicum
