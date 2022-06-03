
# In[1]:
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import warnings
warnings.filterwarnings("ignore")
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

# In[]:
df = pd.read_csv(r'./moyen_data.csv', sep="\t")
# In[]:
df = df[df['class']=='Aves']
# In[]:
df = df[['family','species', 'year', 'month', 'day','decimalLatitude', 'decimalLongitude','individualCount']]
# In[]:
# pour la question 3
#region = pd.read_csv('/Users/clothildedevillenfagne/Cours/Master_2/Memoire/region_obs_oiseaux.csv')
#df['region']=region['0'].tolist()
#df_new = df[df['region']=='Région de Bruxelles-Capitale']

# In[]:
year = set(df['year'].tolist())
#gen = list(set(df['species'].tolist()))
bibliotheque = pd.DataFrame(columns=['antecedents', 'consequents', 'antecedent support', 'consequent support', 'support', 'confidence', 'lift', 'leverage', 'conviction', 'Année'])
for ye in year:
    big_list = []
    data1 = df[df.year == ye].copy()
    print('année :', ye)
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
            for la in latitude:
                lst = []
                final_df = data3[data3.decimalLatitude == la].copy()
                genre = set(final_df['family'].tolist()) # à modifier si on veut que les espèces
                for elem in genre:
                    if pd.isnull(elem) == False:
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

#bibliotheque.to_csv('sol_apriori_00_21.csv', index=False)
# In[]:
# restructuration des données
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
an_ap.to_csv('analyse_apriori_famille.csv', index=False)
# In[]:
df = pd.read_csv(r'/Users/clothildedevillenfagne/Cours/Master_2/Mémoire/sol_apriori_00_21.csv')
# In[]:
anlyse_df = df[df['antecedents'] == "frozenset({'Chroicocephalus ridibundus'})"]
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