from sklearn.neighbors import NearestNeighbors
import numpy as np
from tkinter import *

# Warnung, dass Fenster gefüllt werden müssen, aktuell nur für Feld 1 (Radius), für andere analog 
def button_action():
    entry_text = eingabefeld.get()
    if (entry_text == ""):
        welcome_label.config(text="Geben Sie zuerst einen Wert für Radius ein!")
    else:
        entry_text = "Danke für die Eingabe, bitte auf Lösen klicken!" 
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

#Label für die Eingabebestätigung
welcome_label = Label(fenster)

#Hier kann der Benutzer eine Eingabe machen
eingabefeld = Entry(fenster, bd=5, width=10)
eingabefeld1 = Entry(fenster, bd=5, width=10)
eingabefeld2 = Entry(fenster, bd=5, width=10)
eingabefeld3 = Entry(fenster, bd=5, width=10)
eingabefeld4 = Entry(fenster, bd=5, width=10)

welcom_button = Button(fenster, text="Eingaben prüfen", command=button_action)
exit_button = Button(fenster, text="Lösen", command=fenster.quit)

# Nun fügen wir die Komponenten unserem Fenster hinzu
my_label.grid(row = 0, column = 0)
my_label1.grid(row = 1, column = 0)
my_label2.grid(row = 2, column = 0)
my_label3.grid(row = 3, column = 0)
my_label4.grid(row = 4, column = 0)
eingabefeld.grid(row = 0, column = 1)
eingabefeld1.grid(row = 1, column = 1)
eingabefeld2.grid(row = 2, column = 1)
eingabefeld3.grid(row = 3, column = 1)
eingabefeld4.grid(row = 4, column = 1)
welcom_button.grid(row = 8, column = 0)
exit_button.grid(row = 8, column = 1)
welcome_label.grid(row = 9, column = 1, columnspan = 1)
mainloop()

#Arrays für Normierungsoperationen
min = np.array([1, 30, 1, 90, 50])
range = np.array([14, 70, 19, 110, 950])

#Für festgelegte Werte '#' umsetzen
#inputcase = np.array([[5, 89, 16, 130, 550]])
inputcase = np.array([[14, 98, 18, 193, 841]])
#case = np.array([[0.1, 0.2, 0.3, 0.4, 0.5]])
#inputcase = np.array([[int(eingabefeld.get()), int(eingabefeld1.get()), int(eingabefeld2.get()), int(eingabefeld3.get()), int(eingabefeld4.get())]])

#Normierung der Eingabe
normcase0 = inputcase - min
normcase = normcase0 / range

#Um die Werte in Print nicht als scientific anzuzeigen '#' unten entfernen
np.set_printoptions(suppress=True)

#CSV wird einglesen und in ablagearray abgelegt
with open("studie0702.csv", encoding='utf-8-sig') as file_name:
    ablagearray = np.loadtxt(file_name, delimiter=",")

#Die erste & letzen beiden Spalten im Array werden hiermit gelöscht
arrayzerlegt0 = np.delete(ablagearray, 0, 1)
arrayzerlegt = np.delete(arrayzerlegt0, 6, 1)
arrayzerlegt1 = np.delete(arrayzerlegt, 5, 1)

#Normalisierung der CSV als Array
arraynorm = arrayzerlegt1 - min
arraynorm1 = arraynorm / range

#Normierung für Hilfsebene
min1 = np.array([1, 30, 1, 90, 50, 0, 0])
range1 = np.array([14, 70, 19, 110, 950, 1 ,1])
arrayhilfsebene = arrayzerlegt0 - min1
arrayhilfsebene1 = arrayhilfsebene / range1

#Hiermit wird der nähste Nachbar zwischen case=benutzereingabe und array=csv gefunden (metric=)
nbrs = NearestNeighbors(n_neighbors=1, algorithm='auto').fit(arraynorm1)
distances, indices = nbrs.kneighbors(normcase)

#Hiermit können Nachbarn in einem bestimmten Radius gefunden werden 
neigh = NearestNeighbors(radius=0.45)
neigh.fit(arraynorm1)
rng = neigh.radius_neighbors(normcase)

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
#print ('-----Indices') 
#print (indices)
#print ('-----Distanzen') 
#print (distances)
print("Das ähnlichste Ergebnis ist der Fall mit folgenden Maßen: " + str(arrayzerlegt1[indices]))

#Berechnung für Perzentilangabe
percentsolution = distances
percentil25 = 0.7130
percentil5 = 0.4641
percentil2 = 0.3730
percentil1 = 0.3124

if percentsolution < percentil25:
    per25sol = "Y"
else:
    per25sol = "N"    

if percentsolution < percentil5:
    per5sol = "Y"
else:
    per5sol = "N"    

if percentsolution < percentil2:
    per2sol = "Y"
else:
    per2sol = "N"    

if percentsolution < percentil1:
    per1sol = "Y"
else:
    per1sol = "N"    


#Berechnung über Hilfsebene: (exterpolieren, interpolieren?)
#Einflussstärke auf das Ergebnis:
#faktor
faktor = 1.8868
#vergleichsspannung
seinflussradius = 0.04 * faktor
seinflussbreite = 0 * faktor
seinflussdicke = 0.49 * faktor
seinflusslaenge = 0.03 * faktor
seinflusskraft = 0.16 * faktor
#gesamtverformung
veinflussradius = 0.02 * faktor
veinflussbreite = 0.02 * faktor
veinflussdicke = 0.38 * faktor
veinflusslaenge = 0.02 * faktor
veinflusskraft = 0.09 * faktor

#Für abweichenden Radius
hilfradius = arrayhilfsebene1[indices[0][0]][0] - normcase[0][0]
veinflradius = hilfradius * veinflussradius 
seinflradius = hilfradius * seinflussradius 
if seinflradius >= 0:
    loesungverfradius = arrayhilfsebene1[indices[0][0]][5] * (1 + veinflradius)
    loesungspannradius = arrayhilfsebene1[indices[0][0]][6] * (1 + seinflradius)
else: 
    loesungverfradius = arrayhilfsebene1[indices[0][0]][5] * (1 - veinflradius)
    loesungspannradius = arrayhilfsebene1[indices[0][0]][6] * (1 - seinflradius)

#Für abweichende Breite
hilfbreite = arrayhilfsebene1[indices[0][0]][1] - normcase[0][1]
veinflbreite = hilfbreite * veinflussbreite 
seinflbreite = hilfbreite * seinflussbreite 
if seinflbreite >= 0:
    loesungverfbreite = loesungverfradius * (1 + veinflbreite)
    loesungspannbreite = loesungspannradius * (1 + seinflbreite)
else: 
    loesungverfbreite = loesungverfradius * (1 - veinflbreite)
    loesungspannbreite = loesungspannradius * (1 - seinflbreite)

#Für abweichende Dicke
hilfdicke = arrayhilfsebene1[indices[0][0]][2] - normcase[0][2]
veinfldicke = hilfdicke * veinflussdicke 
seinfldicke = hilfdicke * seinflussdicke 
if seinfldicke >= 0:
    loesungverfdicke = loesungverfbreite * (1 + veinfldicke)
    loesungspanndicke = loesungspannbreite * (1 + seinfldicke)
else: 
    loesungverfdicke = loesungverfbreite * (1 - veinfldicke)
    loesungspanndicke = loesungspannbreite * (1 - seinfldicke)

#Für abweichende Länge
hilflaenge = arrayhilfsebene1[indices[0][0]][3] - normcase[0][3]
veinfllaenge = hilflaenge * veinflusslaenge
seinfllaenge = hilflaenge * seinflusslaenge
if seinfllaenge >= 0:
    loesungverflaenge = loesungverfdicke * (1 + veinfllaenge)
    loesungspannlaenge = loesungspanndicke * (1 + seinfllaenge)
else: 
    loesungverflaenge = loesungverfdicke * (1 - veinfllaenge)
    loesungspannlaenge = loesungspanndicke * (1 - seinfllaenge)

#Für abweichende Kraft
hilfkraft = arrayhilfsebene1[indices[0][0]][4] - normcase[0][4]
veinflkraft = hilfkraft * veinflusskraft 
seinflkraft = hilfkraft * seinflusskraft 
#<> gewechselt
if seinflkraft <= 0:
    loesungverfkraft = loesungverflaenge * (1 + veinflkraft)
    loesungspannkraft = loesungspannlaenge * (1 + seinflkraft)
else: 
    loesungverfkraft = loesungverflaenge * (1 - veinflkraft)
    loesungspannkraft = loesungspannlaenge * (1 - seinflkraft)

print(loesungverfkraft)
print(loesungspannkraft)

#Zweites Fenster für die "Antwort"
ergebnis = Tk()
ergebnis.title("Ergebnis")
ergebnis_label = Label(ergebnis, text="Das ähnlichste Ergebnis ist der Fall mit folgenden Maßen: " + str(arrayzerlegt1[indices]))
ergebnis_label1 = Label(ergebnis, text="Vergleichspannung in MPa:" + str(arrayloesung5[indices]))
ergebnis_label2 = Label(ergebnis, text="Verschiebung in mm:" + str(arrayloesung6[indices]))
ergebnis_label3 = Label(ergebnis, text="Die Distanz beträgt: " + str(distances))
ergebnis_label4 = Label(ergebnis, text="Der Index des ähnlichsten Falls ist: " + str(indices))
ergebnis_label5 = Label(ergebnis, text="Die Lösung liegt innerhalb des 25% Perzentils (Y/N): " + str(per25sol))
ergebnis_label6 = Label(ergebnis, text="Die Lösung liegt innerhalb des 5% Perzentils (Y/N): " + str(per5sol))
ergebnis_label7 = Label(ergebnis, text="Die Lösung liegt innerhalb des 2% Perzentils (Y/N): " + str(per2sol))
ergebnis_label8 = Label(ergebnis, text="Die Lösung liegt innerhalb des 1% Perzentils (Y/N): " + str(per1sol))
ergebnis_label9 = Label(ergebnis, text="Verformung über Hilfsebene: " + str(loesungverfkraft))
ergebnis_label10 = Label(ergebnis, text="Spannung über Hilfsbene " + str(loesungspannkraft))
ergebnis_label.pack()
ergebnis_label1.pack()
ergebnis_label2.pack()
ergebnis_label3.pack()
ergebnis_label4.pack()
ergebnis_label5.pack()
ergebnis_label6.pack()
ergebnis_label7.pack()
ergebnis_label8.pack()
ergebnis_label9.pack()
ergebnis_label10.pack()
ergebnis.mainloop()