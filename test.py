from sklearn.neighbors import NearestNeighbors
from sklearn.neighbors import RadiusNeighborsTransformer
from sklearn.neighbors import *
import numpy as np
import pandas as pd


#CSV wird einglesen und in ablagearray abgelegt
with open("studie.csv", encoding='utf-8-sig') as file_name:
    ablagearray = np.loadtxt(file_name, delimiter=",")
ablagearray[:, [7, 5]] = ablagearray[:, [5, 7]]
ablagearray[:, [7, 6]] = ablagearray[:, [6, 7]]


## convert your array into a dataframe
df = pd.DataFrame (ablagearray)

## save to xlsx file

filepath = 'studievgl.xlsx'

df.to_excel(filepath, index=False)