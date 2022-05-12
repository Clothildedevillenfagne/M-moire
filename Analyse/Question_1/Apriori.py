
# In[1]:
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import warnings
warnings.filterwarnings("ignore")
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

# In[1]:
df = pd.read_csv(r'./data_reduite_obs.csv')
# In[]:
df.columns
print('espèce :', len(set(df['species'].tolist())))
print('genus :', len(set(df['genus'].tolist())))
print('family :', len(set(df['family'].tolist())))
print('order :', len(set(df['order'].tolist())))
print('class :', len(set(df['class'].tolist())))
print('phylum :', len(set(df['phylum'].tolist())))
print('kingdom :', len(set(df['kingdom'].tolist())))
# In[]:
new_df = df[df['class']=='Aves'] # on prend que les oiseau pour comparer c qui est comparable
# In[]:
df["year"].value_counts(normalize=True).plot(kind='pie')
plt.show()
# In[]:
print('espèce :', len(set(new_df['species'].tolist())))
print('genus :', len(set(new_df['genus'].tolist())))
print('family :', len(set(new_df['family'].tolist())))
print('order :', len(set(new_df['order'].tolist())))
# In[]:
# on va regrouper les espèce par genre exemple cigogne noire et blancche vont être mise ensemble
ar = []
year = set(new_df['year'].tolist())
for ye in year:
    new_new_df = new_df[new_df.year == ye].copy()
    genus = set(new_new_df['genus'].tolist())
    count = 0
    print('année :', ye)
    for gn in genus:
        new_new_new_df = new_new_df[new_new_df.genus == gn].copy()
        order = new_new_new_df['order'].tolist()
        family = new_new_new_df['family'].tolist()
        longitude = set(new_new_new_df['decimalLongitude'].tolist())
        print(count)
        count += 1
        for lon in longitude:
            new_new_new_new_df = new_new_new_df[new_new_new_df.decimalLongitude == lon].copy()
            latitude = set(new_new_new_new_df['decimalLatitude'].tolist())
            for la in latitude:  # d'abord refaire un for pour longitude puis latitude
                final_df = new_new_new_new_df[new_new_new_new_df.decimalLatitude == la].copy()
                #num_obs = len(final_df['decimalLatitude'])
                locality = final_df['locality'].tolist()
                stateProvince = final_df['stateProvince'].tolist()
                sums = final_df['individualCount'].sum()
                num_obs = final_df['numberObservation'].sum()
                new_line = [order[0], family[0], gn, locality[0],
                            stateProvince[0], sums, la, lon, ye, num_obs]
                ar.append(new_line)

new_cov = pd.DataFrame(ar, columns=['order', 'family', 'genus', 'locality',
'stateProvince', 'individualCount', 'decimalLatitude', 'decimalLongitude','year', 'numberObservation' ])

# In[]:
# Intializing the list
transacts = []
# populating a list of transactions
for i in range(0, 1494049):
  transacts.append([str(new_cov.values[i,j]) for j in range(0, 10)])
  if i%100:
      print(i)

# In[]:
new_cov.to_csv('data_genre.csv', index=False)

# In[]:
# COMMENCE ICI
df = pd.read_csv(r'/Users/clothildedevillenfagne/Cours/Master_2/Memoire/moyen_data.csv', sep="\t")
# In[]:
df = df[df['class']=='Aves']
# In[]:
df = df[['family','species', 'year', 'month', 'day','decimalLatitude', 'decimalLongitude','individualCount']]
# In[]:
region = pd.read_csv('/Users/clothildedevillenfagne/Cours/Master_2/Memoire/region_obs_oiseaux.csv')
# In[]:
df['region']=region['0'].tolist()
# In[]:
df_new = df[df['region']=='Région de Bruxelles-Capitale']
# In[]:
len(df_new)
# In[]:
#df['month'] = df['month'].replace([1.0, 2.0, 3.0], 1.0)
#df['month'] = df['month'].replace([4.0, 5.0, 6.0], 2.0)
#df['month'] = df['month'].replace([7.0, 8.0, 9.0], 3.0)
#df['month'] = df['month'].replace([10.0, 11.0, 12.0], 4.0)
# In[]:
year = set(df['year'].tolist())
#gen = list(set(df['species'].tolist()))
bibliotheque = pd.DataFrame(columns=['antecedents', 'consequents', 'antecedent support', 'consequent support', 'support', 'confidence', 'lift', 'leverage', 'conviction', 'Année'])
for ye in year:
    big_list = []
    data1 = df[df.year == ye].copy()
    print('année :', ye)
    #print(data1)
    month = set(data1['month'].tolist())
    new_month = []
    count = False
    for elem in month:
        if pd.isnull(elem):
            count = True
        else:
            new_month.append(elem)
        if count == True:
            new_month.append(float('nan'))
    month = new_month
    for mo in month:

        data2 = data1[data1.month == mo].copy()
        longitude = set(data2['decimalLongitude'].tolist())
        print('mois :', mo)
        for lon in longitude:
            data3 = data2[data2.decimalLongitude == lon].copy()
            latitude = set(data3['decimalLatitude'].tolist())
            for la in latitude:  # d'abord refaire un for pour longitude puis latitude
                lst = []#[0] * len(gen) #np.nan
                final_df = data3[data3.decimalLatitude == la].copy()
                #print(final_df)
                # num_obs = len(final_df['decimalLatitude'])
                genre = set(final_df['family'].tolist())
                for elem in genre:
                    if pd.isnull(elem) == False:
                    #index = gen.index(elem)
                    #lst[index]+=1
                        lst.append(elem)

                big_list.append(lst)

    tc = TransactionEncoder()
    DataArry = tc.fit(big_list).transform(big_list)
    BasketSet = pd.DataFrame(DataArry, columns=tc.columns_)
    print(BasketSet.shape)
    frq_items = apriori(BasketSet, min_support=0.1, use_colnames=True)
    rules = association_rules(frq_items, metric="lift", min_threshold=1)
    rules = rules.sort_values(['confidence', 'lift'], ascending=[False, False])
    new_df = rules.assign(Année=ye)
    bibliotheque = pd.concat([bibliotheque, new_df])

# In[]:
#big_list
# In[]:
#big_list.extend(200*[big_list[0]])

#tc = TransactionEncoder()
#DataArry = tc.fit(big_list).transform(big_list)
#BasketSet = pd.DataFrame(DataArry, columns=tc.columns_)

# In[]:
#BasketSet
# In[]:

#frq_items = apriori(BasketSet, min_support = 0.05, use_colnames = True)
#rules = association_rules(frq_items, metric ="lift", min_threshold = 1)
#rules = rules.sort_values(['confidence', 'lift'], ascending =[False, False])
# In[]:
#frq_items
# In[]:
#print(rules.head())
# In[]:
#print(rules)
# In[]:
bibliotheque
# In[]:
bibliotheque.to_csv('sol_apriori_00_21.csv', index=False)
# In[]:
bibliotheque.columns
# In[]:
print(bibliotheque[bibliotheque['antecedents']=='Psittacidae'])
# In[]:
antecedents = set (bibliotheque['antecedents'].tolist())
analyse_apriori = []
count = 0
for ante in antecedents:
    df1 = bibliotheque[bibliotheque['antecedents']==ante]
    consquence = set(df1['consequents'].tolist())
    for cons in consquence:
        df2 = df1[df1['consequents']==cons]
        annee =  []
        for elem in df2.itertuples():
            annee.append(elem.Année)
        nouvel_ligne = [ante, cons, annee, len(annee)]
        analyse_apriori.append(nouvel_ligne)
    count+=1
    if count%100==0:
        print(count)

an_ap = pd.DataFrame(analyse_apriori, columns=['antecedents', 'consequents', 'Année', 'Num_année'])

# In[]:
an_ap = an_ap.sort_values(['Num_année'], ascending =[False])
# In[]:
an_ap


# In[]:
an_ap[an_ap['antecedents'] == frozenset({'Psittacidae'})]['consequents']#
# In[]:
an_ap.to_csv('analyse_apriori_famille.csv', index=False)


# In[]:
df = pd.read_csv(r'/Users/clothildedevillenfagne/Cours/Master_2/Mémoire/sol_apriori_00_21.csv')
# In[]:
anlyse_df = df[df['antecedents'] == "frozenset({'Chroicocephalus ridibundus'})"]
# In[]:
anlyse_df
# In[]:
anlyse_df = anlyse_df[anlyse_df['consequents'] == "frozenset({'Anas platyrhynchos'})"]
# In[]:
sup = anlyse_df['support'].tolist()
year = anlyse_df['Année'].tolist()
plt.figure()
plt.plot(year,sup)
#plt.title("Ratio d'obseervation pour chaque année")
plt.xlabel('Années')
plt.ylabel("Support")
plt.savefig("/Users/clothildedevillenfagne/Cours/Master_2/Mémoire/sup_annee.png")
plt.show

# In[]:
sup = anlyse_df['antecedent support'].tolist()
plt.figure()
plt.plot(year,sup)
#plt.title("Ratio d'obseervation pour chaque année")
plt.xlabel('Années')
plt.ylabel("Support")
plt.savefig("/Users/clothildedevillenfagne/Cours/Master_2/Mémoire/ansup_annee.png")
plt.show

# In[]:
sup = anlyse_df['consequent support'].tolist()
plt.figure()
plt.plot(year,sup)
#plt.title("Ratio d'obseervation pour chaque année")
plt.xlabel('Années')
plt.ylabel("Support")
plt.savefig("/Users/clothildedevillenfagne/Cours/Master_2/Mémoire/cosup_annee.png")
plt.show

# In[]:
sup = anlyse_df['lift'].tolist()
plt.figure()
plt.plot(year,sup)
#plt.title("Ratio d'obseervation pour chaque année")
plt.xlabel('Années')
plt.ylabel("Lift")
plt.savefig("/Users/clothildedevillenfagne/Cours/Master_2/Mémoire/lift_annee.png")
plt.show

# In[]:
sup = anlyse_df['confidence'].tolist()
plt.figure()
plt.plot(year,sup)
#plt.title("Ratio d'observation pour chaque année")
plt.xlabel('Années')
plt.ylabel("confidence")
plt.savefig("/Users/clothildedevillenfagne/Cours/Master_2/Mémoire/conf_annee.png")
plt.show