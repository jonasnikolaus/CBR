from sklearn.neighbors import NearestNeighbors
from sklearn.neighbors import RadiusNeighborsTransformer
from sklearn.neighbors import *
import numpy as np
import pandas as pd

from cbr_normiert_gui import SENSITIVITY
SENSIT = [1, 6, 1, 1, 4]
LAENGE = [90, 200]
DICKE = [1, 20]
RADIUS = [1, 15]
BREITE = [30, 100]
KRAFT = [50, 1000]

minimum = np.array([LAENGE[0], DICKE[0], BREITE[0], RADIUS[0], KRAFT[0]])
range = np.array([LAENGE[1] - LAENGE[0], DICKE[1] - DICKE[0], BREITE[1] - BREITE[0], RADIUS[1] - RADIUS[0], KRAFT[1] - KRAFT[0]])
#normedinput = (input - minimum) / range * SENSITIVITY

#Um die Werte in Print nicht als scientific anzuzeigen '#' unten entfernen
np.set_printoptions(suppress=True)

#CSV wird einglesen und in ablagearray abgelegt
with open("studie2002.csv", encoding='utf-8-sig') as file_name:
    ablagearray = np.loadtxt(file_name, delimiter=",")

#Die erste & letzen beiden Spalten im Array werden hiermit gelöscht

ablagearray[:, [7, 5]] = ablagearray[:, [5, 7]]
ablagearray[:, [7, 6]] = ablagearray[:, [6, 7]]
arrayzerlegt0 = np.delete(ablagearray, 0, 1)
arrayzerlegt = np.delete(arrayzerlegt0, 6, 1)
arrayzerlegt1 = np.delete(arrayzerlegt, 5, 1)



#Normalisierung der CSV als Array
arraynorm0 = arrayzerlegt1 - minimum
arraynorm = arraynorm0 / range
arraynorm1 = arraynorm * SENSIT

#print(arrayzerlegt1[0])
#print(arrayzerlegt1[467])

#case= zeile/y achse
sens = np.arange(250000, dtype='f')

#j= anzhl der zeilen = 468
j = 0
while j < 500:
    i = 0
    
    while i < 500:
        case= arraynorm1[[i]]
        nbrs = NearestNeighbors(n_neighbors=1, algorithm='auto').fit(arraynorm1[[j]])
        distances, indices = nbrs.kneighbors(case)
        sens[j*500+i]= distances
        i += 1
    j +=1
 
print(sens)
sens1= np.reshape(sens, (500, 500)) 
#print(sens1)

## convert your array into a dataframe
df = pd.DataFrame (sens1)

## save to xlsx file

filepath = 'average2302.xlsx'

df.to_excel(filepath, index=False)