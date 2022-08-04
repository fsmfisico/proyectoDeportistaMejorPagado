# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 00:51:31 2022

@author: john
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("D:/Devf/Forbes Richest Atheletes (Forbes Richest Athletes 1990-2020).csv")
nombres = df.columns.values
df1 = df
# df1.info()
# df1.head()
#%%
df1.drop('S.NO',axis=1,inplace=True)
# df1["Previous Year Rank"] = df1["Previous Year Rank"].replace({"not ranked":np.nan})
# df1 = df.dropna()
# df1 = df1.fillna(0)
df1["Sport"]
df1["Sport"] = df["Sport"].str.upper()
# print(df1.head(15))
# %% Deportistas cuyo ranking ha subido al menos dos lugares entre 2010 y 2020.
df2 = df1[(df1.Year >= 2010) & (df1.Year <= 2020)]
nombres_repetidos = np.unique(df2["Name"])
deportistas_Seleccionados = []
for i in range(0,len(nombres_repetidos)):
    df3 = df2[df2.Name == nombres_repetidos[i]]
    shapeData = df3.shape
    for j in range(0, shapeData[0]):
        df4 = df3[j:j+1]
        try:
            df4["Previous Year Rank"] = df4["Previous Year Rank"].astype(int)
            yearNew = int(df4["Current Rank"].iloc[0:1])
            yearPast = int(df4["Previous Year Rank"].iloc[0:1])
            if (yearPast - yearNew) > 2:
                deportistas_Seleccionados.append(nombres_repetidos[i])
                break
        except:
            pass
print("Los deportistas que ha: subido al menos dos lugares entre 2010 y 2020 son: "+str(deportistas_Seleccionados))
# %% Atleta con el menor número de apariciones y mayores ganancias.
nombres_repetidos = np.unique(df1["Name"])
columns = ['Nombre','Frecuencia', 'Ganancia']
df3 = []
for i in range (0,len (nombres_repetidos)):
    df2 = df1[df1.Name == nombres_repetidos[i]]
    frecuencia,_  = df2.shape
    ganancia = sum(df2["earnings ($ million)"])
    df3.append([nombres_repetidos[i],frecuencia,ganancia ])
df3 =  pd.DataFrame(df3, columns=(columns))
df4 = df3[df3.Frecuencia == 1]
maximaGanancia =  df4[df4.Ganancia == df4['Ganancia'].max()] 
print("El atleta con el menor número de apariciones y mayores ganancias. : " + str(maximaGanancia['Nombre'].iloc[0:1]))
# %%Deporte y país con mayor número de atletas no rankeados que entraron en la lista de atletas mejor pagados.
Top_paid_each_year = df1[df1['Current Rank'] == 1].sort_values(by='Year',ascending=False)
df2 = df1[(df1['Previous Year Rank'] == "not ranked") | (df1['Previous Year Rank'].isnull())  | (df1['Previous Year Rank'] == "?") ]
nombres_paid, nombres_ranki= np.unique(Top_paid_each_year["Name"]), np.unique(df2["Name"])
lista_players = []
for i in nombres_paid:
    for j in nombres_ranki:
        if i == j:
            lista_players.append(j)
            print(j)
            break
df3 = pd.DataFrame(columns = ['Nationality','Sport'])
for i in range (0,len(lista_players)):
    bandera = df2[df2.Name == lista_players[i]]
    bandera = bandera[['Nationality','Sport']].head(1)
    df3 = pd.concat([df3, bandera])
deporte, paise= df3.Nationality.value_counts().index, df3.Sport.value_counts().index
print("El deporte {} y país {} tienen el mayor número de atletas no rankeados que entraron en la lista de atletas mejor pagados.".format(paise[0],deporte[0]) )
# %%Ganancia mínima y máxima (dentro del dataset) por deporte y por país.
df3=df1
deportes=np.unique(df3["Sport"])
#print(deportes)
country=np.unique(df3["Nationality"])
#country
for i in range(0,len(deportes)):
  df4= df3[df3["Sport"]==deportes[i]]
  # print(df4)
  for j in range(0,len(country)):
    df5=df4[df4["Nationality"]==country[j]]
    gananciamin= df5["earnings ($ million)"].min()
    gananciamax= df5["earnings ($ million)"].max()
    if np.isnan(gananciamin)  == True | np.isnan(gananciamax)  == True:
        pass
    else:
        print("En el deporte ", deportes[i],"en el País ",country[j],"se obtuvo una ganacia maxima de" , gananciamax,"minima de ",gananciamin) 
# %%País con mayor número de deportes con atletas en el dataset.
dfd = df1.drop_duplicates(subset=['Name'])
dataf=(dfd.groupby(['Nationality','Sport']).agg({'Nationality':'count'}).rename(columns={'Nationality':'count'}).reset_index())
freq = dataf.groupby(['Nationality']).count().sort_values(by='count',ascending=False)
print(freq[:1])
# %% ¿Cuántos atletas por deporte tiene cada país?
dfd = df1.drop_duplicates(subset=['Name'])
dataf=(dfd.groupby(['Nationality','Sport']).agg({'Nationality':'count'}).rename(columns={'Nationality':'count'}).reset_index())
print(dataf)
# %%Atleta con mayores ganancias por deporte por década
df2 = df1
data_reto = []
i = 1990
for i in range (1990,2020,10):
    suma_decada = 0
    df3 = df2[(df2['Year'] < i+10 ) & (df2['Year'] >= i)]
    deporte_repetido = np.unique(df3["Sport"])
    for j in range (0, len(deporte_repetido)):
        df4 = df3[df3['Sport'] == deporte_repetido[j]]
        nombres_repetidos = np.unique(df4["Name"])
        for k in range (0, len(nombres_repetidos)):
            df5 = df4[df4['Name'] == nombres_repetidos[k]]
            suma_decada = sum(df5["earnings ($ million)"])
            data_reto.append([deporte_repetido[j], nombres_repetidos[k],suma_decada])
        data_reto1 = pd.DataFrame(data_reto, columns=("Sport","Name","Total earnings"))
        maxi_val = data_reto1[data_reto1["Total earnings"] == data_reto1["Total earnings"].max()]
        data_reto = []
        print("El atleta {} obtuvo la mayor ganacia en el deporte {}, entre los anos {}-{}".format(maxi_val.iloc[0]['Name'],maxi_val.iloc[0]["Sport"], i,i+10 ))
# %% Ganancia total por cada deporte por cada año.
df2 = df1
data_reto = []
repeated_years = np.unique(df2["Year"])
deporte_repetido = np.unique(df2["Sport"])
for i in range (0, len(repeated_years)):
    df3 = df2[df2['Year'] == repeated_years[0]]
    for j in range(0, len(deporte_repetido)):
        df4 = df3[df3['Sport'] == deporte_repetido[j]]
        ganancia_total = sum(df4['earnings ($ million)'])
        if ganancia_total == 0:
            pass
        else: 
            print("En el año {} en el deporte {} recaudó en total ${:f}".format(repeated_years[i], deporte_repetido[j], ganancia_total))
            data_reto.append([repeated_years[i], deporte_repetido[j], ganancia_total])
data_reto = pd.DataFrame(data_reto, columns=("Year","Sport", "Total earnings"))
