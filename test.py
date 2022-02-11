from sklearn.neighbors import NearestNeighbors
from sklearn.neighbors import RadiusNeighborsTransformer
from sklearn.neighbors import *
import numpy as np

#Arrays für Normierungsoperationen
min = np.array([1, 30, 1, 90, 50])
maxmin = np.array([14, 70, 19, 110, 950])

#Für festgelegte Werte '#' umsetzen
#case1 = np.array([[8, 88, 12, 117, 575]])
case1 = np.array([[10, 64, 2, 171, 527]])
#case1 = np.array([[9, 86, 20, 108, 155]])
#case1 = np.array([[4, 84, 10, 158, 84]])
#case1 = np.array([[11, 60, 15, 148, 909]])
#case = np.array([[0.1, 0.2, 0.3, 0.4, 0.5]])
#case1 = np.array([[int(eingabefeld.get()), int(eingabefeld1.get()), int(eingabefeld2.get()), int(eingabefeld3.get()), int(eingabefeld4.get())]])

#Normierung der Eingabe
case2 = case1 - min
case = case2 / maxmin

#Um die Werte in Print nicht als scientific anzuzeigen '#' unten entfernen
np.set_printoptions(suppress=True)

#CSV wird einglesen und in ablagearray abgelegt
with open("DesignPointLog.csv", encoding='utf-8-sig') as file_name:
    ablagearray = np.loadtxt(file_name, delimiter=",")

#Die erste & letzen beiden Spalten im Array werden hiermit gelöscht
arrayzerlegt0 = np.delete(ablagearray, 0, 1)
arrayzerlegt = np.delete(arrayzerlegt0, 6, 1)
arrayzerlegt1 = np.delete(arrayzerlegt, 5, 1)

#Normalisierung der CSV als Array
arraynorm = arrayzerlegt1 - min
arraynorm1 = arraynorm / maxmin

#Hiermit wird der nähste Nachbar zwischen case=benutzereingabe und array=csv gefunden
#Metric= The distance metric to use for the tree. The default metric is minkowski, and with p=2 is equivalent to the standard Euclidean metric.
#“euclidean”
#EuclideanDistance
#sqrt(sum((x - y)^2))
#“manhattan”
#ManhattanDistance
#sum(|x - y|)
#“chebyshev”
#ChebyshevDistance
#max(|x - y|)
#“minkowski”
#MinkowskiDistance
#p, w
#sum(w * |x - y|^p)^(1/p)
#“wminkowski”
#WMinkowskiDistance
#p, w
#sum(|w * (x - y)|^p)^(1/p)
#“seuclidean”
#SEuclideanDistance
#V
#sqrt(sum((x - y)^2 / V))
#“mahalanobis”
#MahalanobisDistance
#V or VI
#sqrt((x - y)' V^-1 (x - y))

nbrs = NearestNeighbors(n_neighbors=3, algorithm='auto', metric='minkowski', p=1).fit(arraynorm1)
distances, indices = nbrs.kneighbors(case)

#Test
print("-----Lösung------")
print("Das ähnlichste Ergebnis ist der Fall mit folgenden Maßen: " + str(arrayzerlegt1[indices]))

#Das Array wird weiter zerlegt um Spannung und Verformung auszudrücken
arrayloesung = np.delete(arrayzerlegt0, 0, 1)
arrayloesung1 = np.delete(arrayloesung, 0, 1)
arrayloesung2 = np.delete(arrayloesung1, 0, 1)
arrayloesung3 = np.delete(arrayloesung2, 0, 1)
arrayloesung4 = np.delete(arrayloesung3, 0, 1)
arrayloesung5 = np.delete(arrayloesung4, 0, 1)
arrayloesung6 = np.delete(arrayloesung4, 1, 1)

#Test
print("Vergleichspannung in MPa:" + str(arrayloesung5[indices]))
print("Verschiebung in mm:" + str(arrayloesung6[indices]))
#Test, nicht nötig
print ('-----Indices/ Index') 
print (indices)
print ('-----Distanz/ en') 
print (distances)

#NEU!!!
neigh = NearestNeighbors(radius=0.4)
neigh.fit(arraynorm1)
rng = neigh.radius_neighbors(case)

#print("Distanz zu allen Punkten die Näher sind als der eingegebene Radius")
#print(np.asarray(rng[0][0]))
#print("Indices der Punkte")
#print(np.asarray(rng[1][0]))
#print("Das ähnlichste Ergebnis ist der Fall mit folgenden Maßen: " + str(arrayzerlegt1[439]))
#print("Das ähnlichste Ergebnis ist der Fall mit folgenden Maßen: " + str(arrayzerlegt1[124]))
