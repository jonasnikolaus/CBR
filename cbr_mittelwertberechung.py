from numpy.typing import _128Bit
from sklearn.neighbors import NearestNeighbors
import numpy as np
from tkinter import *

# Warnung, dass Fenster gefüllt werden müssen, aktuell nur für Feld 1 (Radius), für andere analog 
def button_action():
    entry_text = eingabefeld.get()
    if (entry_text == ""):
        welcome_label.config(text="Geben Sie zuerst alle Werte ein")
    else:
        entry_text = "Danke für die Eingabe, bitte auf Beenden klicken!" 
        welcome_label.config(text=entry_text)

#Fenster erstellen
fenster = Tk()
fenster.title("Bitte geben Sie die Maße in der Maske ein")

#Anweisungs-Label
my_label = Label(fenster, text="Radius in mm:   (1-15)")
my_label1 = Label(fenster, text="Breite in mm:  (30-100)")
my_label2 = Label(fenster, text="Dicke in mm:   (1-20)")
my_label3 = Label(fenster, text="Länge in mm:   (90-200)")
my_label4 = Label(fenster, text="Kraft in N:    (50-1000)")
#my_label5 = Label(fenster, text="Gesamtverformung")
#my_label6 = Label(fenster, text="Vergleichsspannung")
#my_label7 = Label(fenster, text="DP")

#Label für die Eingabebestätigung
welcome_label = Label(fenster)

#Hier kann der Benutzer eine Eingabe machen
eingabefeld = Entry(fenster, bd=5, width=10)
eingabefeld1 = Entry(fenster, bd=5, width=10)
eingabefeld2 = Entry(fenster, bd=5, width=10)
eingabefeld3 = Entry(fenster, bd=5, width=10)
eingabefeld4 = Entry(fenster, bd=5, width=10)
#eingabefeld5 = Entry(fenster, bd=5, width=40)
#eingabefeld6 = Entry(fenster, bd=5, width=40)
#eingabefeld7 = Entry(fenster, bd=5, width=40)

welcom_button = Button(fenster, text="Bestätigen", command=button_action)
exit_button = Button(fenster, text="Beenden", command=fenster.quit)

# Nun fügen wir die Komponenten unserem Fenster hinzu
my_label.grid(row = 0, column = 0)
my_label1.grid(row = 1, column = 0)
my_label2.grid(row = 2, column = 0)
my_label3.grid(row = 3, column = 0)
my_label4.grid(row = 4, column = 0)
#my_label5.grid(row = 5, column = 0)
#my_label6.grid(row = 6, column = 0)
#my_label7.grid(row = 7, column = 0)
eingabefeld.grid(row = 0, column = 1)
eingabefeld1.grid(row = 1, column = 1)
eingabefeld2.grid(row = 2, column = 1)
eingabefeld3.grid(row = 3, column = 1)
eingabefeld4.grid(row = 4, column = 1)
#eingabefeld5.grid(row = 5, column = 1)
#eingabefeld6.grid(row = 6, column = 1)
#eingabefeld7.grid(row = 7, column = 1)
welcom_button.grid(row = 8, column = 0)
exit_button.grid(row = 8, column = 1)
welcome_label.grid(row = 9, column = 1, columnspan = 1)
mainloop()

#Arrays für Normierungsoperationen
min = np.array([1, 30, 1, 90, 50])
maxmin = np.array([14, 70, 19, 110, 950])

#Für festgelegte Werte '#' umsetzen
#case1 = np.array([[5, 89, 16, 130, 550]])
#case = np.array([[0.1, 0.2, 0.3, 0.4, 0.5]])
case1 = np.array([[int(eingabefeld.get()), int(eingabefeld1.get()), int(eingabefeld2.get()), int(eingabefeld3.get()), int(eingabefeld4.get())]])

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

#Hiermit wird der nähste Nachbar zwischen case=benutzereingabe und array=csv gefunden (metric=)
nbrs = NearestNeighbors(n_neighbors=5, algorithm='auto').fit(arraynorm1)
distances, indices = nbrs.kneighbors(case)

#Hiermit können Nachbarn in einem bestimmten Radius gefunden werden 
neigh = NearestNeighbors(radius=0.45)
neigh.fit(arraynorm1)
rng = neigh.radius_neighbors(case)

#Distanz zu allen Punkten die Näher sind als der eingegebene Radius
print("------LÖSUNG-------")
print("Distanz zu allen Punkten die Näher sind als der eingegebene Radius")
print(np.asarray(rng[0][0]))

#Indices der Punkte
print("Indices der Punkte")
print(np.asarray(rng[1][0]))


#Hilfe um nahe Arrays anzuzeigen
#print("Das ähnlichste Ergebnis ist der Fall mit folgenden Maßen: " + str(arrayzerlegt1[439]))
#print("Das ähnlichste Ergebnis ist der Fall mit folgenden Maßen: " + str(arrayzerlegt1[124]))


#Das Array wird weiter zerlegt um Spannung und Verformung auszudrücken(print)
arrayloesung = np.delete(arrayzerlegt0, 0, 1)
arrayloesung1 = np.delete(arrayloesung, 0, 1)
arrayloesung2 = np.delete(arrayloesung1, 0, 1)
arrayloesung3 = np.delete(arrayloesung2, 0, 1)
arrayloesung4 = np.delete(arrayloesung3, 0, 1)
arrayloesung5 = np.delete(arrayloesung4, 0, 1)
arrayloesung6 = np.delete(arrayloesung4, 1, 1)

#Test
#print("Vergleichspannung in MPa:" + str(arrayloesung5[indices]))
#print("Verschiebung in mm:" + str(arrayloesung6[indices]))
#Test, nicht nötig
print ('-----Indices') 
print (indices)
print ('-----Distanzen') 
print (distances)
print("Das ähnlichste Ergebnis ist der Fall mit folgenden Maßen: " + str(arrayzerlegt1[indices]))

#Zweites Fenster für die "Antwort"
ergebnis = Tk()
ergebnis.title("Ergebnis")
ergebnis_label = Label(ergebnis, text="Das ähnlichste Ergebnis ist der Fall mit folgenden Maßen: " + str(arrayzerlegt1[indices]))
ergebnis_label1 = Label(ergebnis, text="Vergleichspannung in MPa:" + str(arrayloesung5[indices]))
ergebnis_label2 = Label(ergebnis, text="Verschiebung in mm:" + str(arrayloesung6[indices]))
ergebnis_label3 = Label(ergebnis, text="Die Distanz beträgt: " + str(distances))
ergebnis_label4 = Label(ergebnis, text="Der Index des ähnlichsten Falls ist: " + str(indices))
ergebnis_label.pack()
ergebnis_label1.pack()
ergebnis_label2.pack()
ergebnis_label3.pack()
ergebnis_label4.pack()
ergebnis.mainloop()

#für case feste werte ohne eingabe getestet
aeingabe = case1[0][2]
aloesung = arrayzerlegt0[indices[0][1]][2]
bloesung = arrayzerlegt0[indices[0][0]][2]

if aloesung < aeingabe and bloesung > aeingabe:
    print("Mitte kann berechnet werden")
    mitteverf = (arrayzerlegt0[indices[0][0]][5] + arrayzerlegt0[indices[0][1]][5]) / 2
    mittespann = (arrayzerlegt0[indices[0][0]][6] +arrayzerlegt0[indices[0][1]][6]) / 2
    print("Mittlere Verformung: " + str(mitteverf))
    print("Mittlere Spannung: " + str(mittespann))

if aloesung > aeingabe and bloesung < aeingabe:
    print("Mitte kann berechnet werden")
    mitteverf = (arrayzerlegt0[indices[0][0]][5] + arrayzerlegt0[indices[0][1]][5]) / 2
    mittespann = (arrayzerlegt0[indices[0][0]][6] +arrayzerlegt0[indices[0][1]][6]) / 2
    print("Mittlere Verformung: " + str(mitteverf))
    print("Mittlere Spannung: " + str(mittespann))

if aloesung == aeingabe or bloesung == aeingabe:
    print("Mitte kann nicht berechnet werden (gleiche Materialstärke)")
    if aloesung == aeingabe:
        print("Verformung: " + str(arrayzerlegt0[indices[0][1]][5]))
        print("Spannung: " + str(arrayzerlegt0[indices[0][1]][6]))
    else: 
        print("Verformung: " + str(arrayzerlegt0[indices[0][0]][5]))
        print("Spannung: " + str(arrayzerlegt0[indices[0][0]][6]))

"""
print("Mittelwert")
print(arrayzerlegt0[indices[0][0]])
print(arrayzerlegt0[indices[0][1]])
#"""