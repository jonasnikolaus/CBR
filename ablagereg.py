from sklearn.neighbors import NearestNeighbors
import numpy as np
import PySimpleGUI as pg
import re
from sklearn.linear_model import LinearRegression

STUDIE = "DesignPointLog.csv"
EINGABE = "vergleich.csv"
PERCENTIL25 = 1.7865
PERCENTIL5 = 0.9812
PERCENTIL2 = 0.7683
PERCENTIL1 = 0.6465
PERCENTIL05 = 0.5468
PERCENTIL01 = 0.3839
SENSITIVITY = [1, 6, 1, 1, 4]
# [minimum, maximum]
LAENGE = [90, 200]
DICKE = [1, 20]
RADIUS = [1, 15]
BREITE = [30, 100]
KRAFT = [50, 1000]

FONT_SIZE = ("Arial", 18)
LAYOUT = [[
    pg.Column([[
        pg.Column([
            [pg.Text("Länge in mm:   (90-200)  ")],
            [pg.Text("Dicke in mm:   (1-20)    ")],
            [pg.Text("Breite in mm:  (30-100)  ")],
            [pg.Text("Radius in mm:  (1-15)    ")],
            [pg.Text("Kraft in N:    (50-1000) ")],
            [pg.Text("Nachbarn innerhalb des Radius: ")],
        ]),
        pg.Column([
            [pg.Input(150, size=(4, 1), key="-Laenge-")],
            [pg.Input(10, size=(4, 1), key="-Dicke-")],
            [pg.Input(50, size=(4, 1), key="-Breite-")],
            [pg.Input(10, size=(4, 1), key="-Radius-")],
            [pg.Input(500, size=(4, 1), key="-Kraft-")],
            [pg.Input(1.5, size=(4, 1), key="-Radiussuche-")],
        ]),
        ],
        [
            pg.Button("Berechnen", key='-Berechnen-')
        ]]),
    pg.Column([[
        pg.Column([
            [pg.Text("Das ähnlichste Ergebnis hat folgende Maße:")],
            [pg.Text("Vergleichsspannung in MPa:")],
            [pg.Text("Verschiebung in mm:")],
            [pg.Text("Die Distanz beträgt:")],
            [pg.Text("Der Index des ähnlichsten Falls ist:")],
            [pg.Text("Die Lösung liegt innerhalb des Perzentils:")],
            [pg.Text("Vorhergesagte Verformung:")],
            [pg.Text("Vorhergesagte Spannung:")],
            [pg.Text("Distanz zu Fällen im Radius:", size=(25,2))],
            [pg.Text("Indices der Fälle:", size=(25,2))],
        ]),
        pg.Column([
            [pg.Text("", key='-Ergebnis-Aehnlich-', size=(25,1))],
            [pg.Text("", key='-Ergebnis-Vergleichsspannung-', size=(25,1))],
            [pg.Text("", key='-Ergebnis-Verschiebung-', size=(25,1))],
            [pg.Text("", key='-Ergebnis-Distanz-', size=(25,1))],
            [pg.Text("", key='-Ergebnis-Index-', size=(25,1))],
            [pg.Text("", key='-Ergebnis-Perzentil-', size=(25,1))],
            [pg.Text("", key='-Ergebnis-Verformung-', size=(25,1))],
            [pg.Text("", key='-Ergebnis-Spannung-', size=(25,1))],
            [pg.Text("", key='-Ergebnis-Radiusfaelle-', size=(25,2))],
            [pg.Text("", key='-Ergebnis-Radiusdistanzen-', size=(25,2))],
        ]),
        ],
        [
        ]])
]]

# Entry point
def main():
    # Fenster erstellen
    fenster = pg.Window("Case-Based Reasoning", LAYOUT, font=FONT_SIZE)
    
    # Programmablauf
    while True:
        # Warte auf Events
        event, values = fenster.read()
        
        # Fenster schließen
        if event == pg.WIN_CLOSED:
            exit(0)

        # Berechnung beginnen
        if event == '-Berechnen-':
            # User Input in Array kopieren
            np.set_printoptions(suppress=True)

            with open(EINGABE, encoding='utf-8-sig') as file_name:
                eingabe = np.loadtxt(file_name, delimiter=",")

            eingabe[:, [7, 5]] = eingabe[:, [5, 7]]
            eingabe[:, [7, 6]] = eingabe[:, [6, 7]]
            eingabezerlegt0 = np.delete(eingabe, 0, 1)
            eingabezerlegt = np.delete(eingabezerlegt0, 6, 1)
            eingabezerlegt1 = np.delete(eingabezerlegt, 5, 1)
            

            #input = np.array([[int(values['-Laenge-']), int(values['-Dicke-']), int(values['-Breite-']), int(values['-Radius-']), int(values['-Kraft-'])]])
            
            # Normierung der Eingabe
            minimum = np.array([LAENGE[0], DICKE[0], BREITE[0], RADIUS[0], KRAFT[0]])
            range = np.array([LAENGE[1] - LAENGE[0], DICKE[1] - DICKE[0], BREITE[1] - BREITE[0], RADIUS[1] - RADIUS[0], KRAFT[1] - KRAFT[0]])
            #print(minimum)
            #print(range)
            #print(SENSITIVITY)

            durchgang = 0
            while durchgang < 5:

                print("Durchgang")
                durchgang = durchgang + 1

            # 0 muss mit buchstabe ersetzt werden
            normedinput = (eingabezerlegt1[[0]] - minimum) / range * SENSITIVITY
            input = eingabezerlegt1[[0]]

            #print(normedinput)
            print(eingabezerlegt1[0])
            # Um die Werte in Print nicht als scientific anzuzeigen '#' unten entfernen
            np.set_printoptions(suppress=True)

            # CSV wird einglesen und in ablagearray abgelegt
            with open(STUDIE, encoding='utf-8-sig') as file_name:
                ablagearray = np.loadtxt(file_name, delimiter=",")
            
            # Hiermit werden zwei Spalten im Array ausgetauscht
            ablagearray[:, [7, 5]] = ablagearray[:, [5, 7]]
            ablagearray[:, [7, 6]] = ablagearray[:, [6, 7]]

            # Die erste & letzen beiden Spalten im Array werden hiermit gelöscht
            arrayzerlegt0 = np.delete(ablagearray, 0, 1)
            arrayzerlegt = np.delete(arrayzerlegt0, 6, 1)
            arrayzerlegt1 = np.delete(arrayzerlegt, 5, 1)

            # Normalisierung der CSV als Array
            arraynorm = (arrayzerlegt1 - minimum) / range * SENSITIVITY

            # Hiermit wird der nähste Nachbar zwischen case=benutzereingabe und array=csv gefunden (metric=)
            nbrs = NearestNeighbors(n_neighbors=10, algorithm='auto').fit(arraynorm)
            distances, indices = nbrs.kneighbors(normedinput)

            # Hiermit können Nachbarn in einem bestimmten Radius gefunden werden 
            neigh = NearestNeighbors(radius=float(values['-Radiussuche-']))
            neigh.fit(arraynorm)
            rng = neigh.radius_neighbors(normedinput)

            # Distanz zu allen Punkten die Näher sind als der eingegebene Radius
            print("------LÖSUNG-------")
            #print("Distanz zu allen Punkten, die näher sind als der eingegebene Radius")
            #print(np.asarray(rng[0][0]))

            # Indices der Punkte
            #print("Indices der Punkte")
            #print(np.asarray(rng[1][0]))

            # Das Array wird weiter zerlegt um Spannung und Verformung auszudrücken(print)
            arrayloesung = np.delete(arrayzerlegt0, 0, 1)
            arrayloesung1 = np.delete(arrayloesung, 0, 1)
            arrayloesung2 = np.delete(arrayloesung1, 0, 1)
            arrayloesung3 = np.delete(arrayloesung2, 0, 1)
            arrayloesung4 = np.delete(arrayloesung3, 0, 1)
            arrayloesung5 = np.delete(arrayloesung4, 0, 1)
            arrayloesung6 = np.delete(arrayloesung4, 1, 1)

            # Test
            #print("Vergleichsspannung in MPa:" + str(arrayloesung5[indices]))
            #print("Verschiebung in mm:" + str(arrayloesung6[indices]))
            #Test, nicht nötig
            #print ('-----Indices') 
            #print (indices)
            #print ('-----Distanzen') 
            #print (distances)
            #print("Das ähnlichste Ergebnis ist der Fall mit folgenden Maßen: " + str(arrayzerlegt1[indices]))

            # Nur die Distanz zum nähsten Fall
            distanz = distances[0][0]

            # Berechnung für Perzentilangabe
            percentsolution = ">25%"
            if distanz < PERCENTIL25:    
                percentsolution = "25%"
            if distanz < PERCENTIL5:    
                percentsolution = "5%"
            if distanz < PERCENTIL2:
                percentsolution = "2%"
            if distanz < PERCENTIL1:    
                percentsolution = "1%"
            if distanz < PERCENTIL05:
                percentsolution = "0.5%"
            if distanz < PERCENTIL01:
                percentsolution = "0.1%"
            #"""
            # Lineare Regression Verformung
            X = arrayzerlegt1[indices]
            y = arrayloesung6[indices]

            nsamples, nx, ny = X.shape
            d2_train_dataset = X.reshape((nsamples, nx*ny))
            d22 = d2_train_dataset.reshape((10, 5))

            nsol, mx, my = y.shape
            e2_train_dataset = y.reshape((nsol, mx*my))
            e22 = e2_train_dataset.reshape((10, 1))

            regverf = LinearRegression().fit(d22, e22)
            #print(regverf.score(d22, e22))
            regverfpred = regverf.predict(input)
            #print(regverfpred)

            # Lineare Regression Spannung
            X1 = arrayzerlegt1[indices]
            y1 = arrayloesung5[indices]

            n1samples, nx1, ny1 = X1.shape
            d21_train_dataset = X1.reshape((n1samples, nx1*ny1))
            d221 = d21_train_dataset.reshape((10, 5))

            n1sol, mx1, my1 = y1.shape
            e21_train_dataset = y1.reshape((n1sol, mx1*my1))
            e221 = e21_train_dataset.reshape((10, 1))

            regspann = LinearRegression().fit(d221, e221)
            #print(regspann.score(d221, e221))
            regspannpred = regspann.predict(input)
            #print(regspannpred)
            
            #"""

            # Ergebnisse anzeigen
            # re.sub() wird genutzt um manche Ergebnisse ohne Klammern anzuzeigen
            fenster['-Ergebnis-Aehnlich-'].update(re.sub('[\[\]]', '', np.array2string(arrayzerlegt1[indices])))
            fenster['-Ergebnis-Vergleichsspannung-'].update(re.sub('[\[\]]', '', np.array2string(arrayloesung5[indices])))
            fenster['-Ergebnis-Verschiebung-'].update(re.sub('[\[\]]', '', np.array2string(arrayloesung6[indices])))
            fenster['-Ergebnis-Distanz-'].update(re.sub('[\[\]]', '', np.array2string(distances[0][0])))
            fenster['-Ergebnis-Index-'].update(re.sub('[\[\]]', '', np.array2string(indices[0][0])))
            fenster['-Ergebnis-Perzentil-'].update(percentsolution)
            fenster['-Ergebnis-Verformung-'].update(re.sub('[\[\]]', '', np.array2string(regverfpred)))
            fenster['-Ergebnis-Spannung-'].update(re.sub('[\[\]]', '', np.array2string(regspannpred)))
            fenster['-Ergebnis-Radiusfaelle-'].update(re.sub('[\[\]]', '', np.array2string(np.asarray(rng[0][0]))))
            fenster['-Ergebnis-Radiusdistanzen-'].update(re.sub('[\[\]]', '', np.array2string(np.asarray(rng[1][0]))))

        fenster.refresh()

# Wird gebraucht um main zu starten 
if __name__ == "__main__":
    main()