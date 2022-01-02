from sklearn.neighbors import NearestNeighbors
from sklearn.neighbors import RadiusNeighborsTransformer
from sklearn.neighbors import *
import numpy as np
import pandas as pd

#Arrays für Normierungsoperationen
min = np.array([1, 30, 1, 90, 50])
maxmin = np.array([14, 70, 19, 110, 950])

np.set_printoptions(suppress=True)
with open("DesignPointLog.csv", encoding='utf-8-sig') as file_name:
    ablagearray = np.loadtxt(file_name, delimiter=",")
arrayzerlegt0 = np.delete(ablagearray, 0, 1)
arrayzerlegt = np.delete(arrayzerlegt0, 6, 1)
arrayzerlegt1 = np.delete(arrayzerlegt, 5, 1)
arraynorm = arrayzerlegt1 - min
arraynorm1 = arraynorm / maxmin
#print(arraynorm1)
#print(case1)
#print(ablagearray[0])
#print(case)
#print(arrayzerlegt1[0])
#print(arrayzerlegt1[467])

#case= zeile/y achse
sens = np.arange(219024, dtype='f')

#j= anzhl der zeilen = 468
j = 0
while j < 468:
    i = 0
    
    while i < 468:
        case= arraynorm1[[i]]
        nbrs = NearestNeighbors(n_neighbors=1, algorithm='auto').fit(arraynorm1[[j]])
        distances, indices = nbrs.kneighbors(case)
        sens[j*468+i]= distances
        i += 1
    j +=1
 
print(sens)
sens1= np.reshape(sens, (468, 468)) 
#print(sens1)

## convert your array into a dataframe
df = pd.DataFrame (sens1)

## save to xlsx file

filepath = 'sensitivity.xlsx'

df.to_excel(filepath, index=False)