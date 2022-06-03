#!/usr/bin/env python
# coding: utf-8

# # Animal evolution in Belgium

# #### <br> Visualize the data base

# In[]:
import pandas as pd

# In[]:
df = pd.read_csv(r'./data.csv', sep="\t")

# In[]:
df = df[['kingdom', 'phylum', 'class','order', 'family', 'genus', 'species','locality','stateProvince',
         'individualCount', 'decimalLatitude', 'decimalLongitude','year']]

# In[]:
year = set(df['year'].tolist())

# In[]:
ar = []
for ye in year:
    new_df = df[df.year == ye].copy()
    species = set(new_df['species'].tolist())
    count = 0
    print('année :', ye)
    for sp in species:
        new_new_df = new_df[new_df.species == sp].copy()
        kingdom = new_new_df['kingdom'].tolist()
        phylum = new_new_df['phylum'].tolist()
        class_sp = new_new_df['class'].tolist()
        order = new_new_df['order'].tolist()
        family = new_new_df['family'].tolist()
        genus = new_new_df['genus'].tolist()
        longitude = set(new_new_df['decimalLongitude'].tolist())
        print(count)
        count+=1
        for lon in longitude:
            new_new_new_df = new_new_df[new_new_df.decimalLongitude == lon].copy()
            latitude = set(new_new_new_df['decimalLatitude'].tolist())
            for la in latitude: # d'abord refaire un for pour longitude puis latitude
                final_df = new_new_new_df[new_new_new_df.decimalLatitude == la].copy()
                num_obs = len(final_df['decimalLatitude'])
                locality = final_df['locality'].tolist()
                stateProvince = final_df['stateProvince'].tolist()
                sums = final_df['individualCount'].sum()
                new_line = [kingdom[0], phylum[0], class_sp[0], order[0], family[0], genus[0], sp, locality[0], stateProvince[0], sums, la, lon, ye, num_obs]
                ar.append(new_line)

new_cov = pd.DataFrame(ar, columns=['kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species', 'locality',
                                    'stateProvince', 'individualCount', 'decimalLatitude', 'decimalLongitude','year', 'numberObservation' ])
# In[]:
# passer de 22563396 à 5196751
new_cov.to_csv('data_reduite_obs.csv', index=False)

# In[]:
df = pd.read_csv(r'./data_reduite_obs.csv')
# In[]:
len(set(df['numberObservation'].tolist()))
# In[]:
liste_espece = set(df['species'].tolist())
print(liste_espece)

# In[]:
all_list = pd.DataFrame(liste_espece, columns=['species'])
print(all_list)
# In[]:
all_list.to_csv('liste_espece.csv', index=False)