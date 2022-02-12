from sklearn.neighbors import NearestNeighbors
import numpy as np
import PySimpleGUI as pg
import re

PERCENTIL25 = 0.7130
PERCENTIL5 = 0.4641
PERCENTIL2 = 0.3730
PERCENTIL1 = 0.3124
PERCENTIL05 = 0.2693
PERCENTIL01 = 0.1886

# [minimum, maximum]
RADIUS = [1, 15]
BREITE = [30, 100]
DICKE = [1, 20]
LAENGE = [90, 200]
KRAFT = [50, 1000]

FONT_SIZE = ("Arial", 18)
LAYOUT = [[
    pg.Column([[
        pg.Column([
            [pg.Text("Radius in mm:  (1-15)    ")],
            [pg.Text("Breite in mm:  (30-100)  ")],
            [pg.Text("Dicke in mm:   (1-20)    ")],
            [pg.Text("Länge in mm:   (90-200)  ")],
            [pg.Text("Kraft in N:    (50-1000) ")],
        ]),
        pg.Column([
            [pg.Input(RADIUS[0], size=(4, 1), key="-Radius-")],
            [pg.Input(BREITE[0], size=(4, 1), key="-Breite-")],
            [pg.Input(DICKE[0], size=(4, 1), key="-Dicke-")],
            [pg.Input(LAENGE[0], size=(4, 1), key="-Laenge-")],
            [pg.Input(KRAFT[0], size=(4, 1), key="-Kraft-")],
        ]),
        ],
        [
            pg.Button("Berechnen", key='-Berechnen-')
        ]]),
    pg.Column([[
        pg.Column([
            [pg.Text("Das ähnlichste Ergebnis ist der Fall mit folgenden Maßen:")],
            [pg.Text("Vergleichspannung in MPa:")],
            [pg.Text("Verschiebung in mm:")],
            [pg.Text("Die Distanz beträgt:")],
            [pg.Text("Der Index des ähnlichsten Falls ist:")],
            [pg.Text("Die Lösung liegt innerhalb des Perzentil")],
            [pg.Text("Verformung über Hilfsebene:")],
            [pg.Text("Spannung über Hilfsbene:")],
        ]),
        pg.Column([
            [pg.Text("", key='-Ergebnis-Aehnlich-', size=(25,1))],
            [pg.Text("", key='-Ergebnis-Vergleichspannung-')],
            [pg.Text("", key='-Ergebnis-Verschiebung-')],
            [pg.Text("", key='-Ergebnis-Distanz-')],
            [pg.Text("", key='-Ergebnis-Index-')],
            [pg.Text("", key='-Ergebnis-Perzentil-')],
            [pg.Text("", key='-Ergebnis-Verformung-')],
            [pg.Text("", key='-Ergebnis-Spannung-')],
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
            input = np.array([[int(values['-Radius-']), int(values['-Breite-']),int(values['-Dicke-']), int(values['-Laenge-']), int(values['-Kraft-'])]])

            # Normierung der Eingabe
            minimum = np.array([RADIUS[0], BREITE[0], DICKE[0], LAENGE[0], KRAFT[0]])
            range = np.array([RADIUS[1] - RADIUS[0], BREITE[1] - BREITE[0], DICKE[1] - DICKE[0], LAENGE[1] - LAENGE[0], KRAFT[1] - KRAFT[0]])
            normedinput = (input - minimum) / range

            # Um die Werte in Print nicht als scientific anzuzeigen '#' unten entfernen
            np.set_printoptions(suppress=True)

            # CSV wird einglesen und in ablagearray abgelegt
            with open("studie0702.csv", encoding='utf-8-sig') as file_name:
                ablagearray = np.loadtxt(file_name, delimiter=",")

            # Die erste & letzen beiden Spalten im Array werden hiermit gelöscht
            arrayzerlegt0 = np.delete(ablagearray, 0, 1)
            arrayzerlegt = np.delete(arrayzerlegt0, 6, 1)
            arrayzerlegt1 = np.delete(arrayzerlegt, 5, 1)

            # Normalisierung der CSV als Array
            arraynorm = (arrayzerlegt1 - minimum) / range

            # Normierung für Hilfsebene
            min1 = np.array([1, 30, 1, 90, 50, 0, 0])
            range1 = np.array([14, 70, 19, 110, 950, 1 ,1])
            arrayhilfsebene = arrayzerlegt0 - min1
            arrayhilfsebene1 = arrayhilfsebene / range1

            # Hiermit wird der nähste Nachbar zwischen case=benutzereingabe und array=csv gefunden (metric=)
            nbrs = NearestNeighbors(n_neighbors=1, algorithm='auto').fit(arraynorm)
            distances, indices = nbrs.kneighbors(normedinput)

            # Hiermit können Nachbarn in einem bestimmten Radius gefunden werden 
            neigh = NearestNeighbors(radius=0.45)
            neigh.fit(arraynorm)
            rng = neigh.radius_neighbors(normedinput)

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

            # Berechnung für Perzentilangabe
            percentsolution = ">25%"
            if distances < PERCENTIL25:    
                percentsolution = "25%"
            if distances < PERCENTIL5:    
                percentsolution = "5%"
            if distances < PERCENTIL2:
                percentsolution = "2%"
            if distances < PERCENTIL1:    
                percentsolution = "1%"
            if distances < PERCENTIL05:
                percentsolution = "0.5%"
            if distances < PERCENTIL01:
                percentsolution = "0.1%"
            
            #Berechnung über Hilfsebene: (exterpolieren, interpolieren?)
            #Einflussstärke auf das Ergebnis:

            #vergleichsspannung
            seinflussradius = 0
            seinflussbreite = 0
            seinflussdicke = 0
            seinflusslaenge = 0
            seinflusskraft = 0
            #gesamtverformung
            veinflussradius = 0
            veinflussbreite = 0
            veinflussdicke = 0
            veinflusslaenge = 0
            veinflusskraft = 0

            #Für abweichenden Radius
            hr = arrayhilfsebene1[indices[0][0]][0] * 10
            hr1 = normedinput[0][0] * 10
            hrber = (30.985 * hr) ** (-0.322)
            hrber1 = (30.985 * hr1) ** (-0.322)
            hrber2 = hrber / hrber1

            if hrber2 > 1:
                loesungverfradius = arrayhilfsebene1[indices[0][0]][5] / (hrber2 * (1 + veinflussradius))
                loesungspannradius = arrayhilfsebene1[indices[0][0]][6] / (hrber2 * (1 + seinflussradius))
            else: 
                if hrber2 == 1:
                    loesungverfradius = arrayhilfsebene1[indices[0][0]][5]
                    loesungspannradius = arrayhilfsebene1[indices[0][0]][6]
                else:
                    loesungverfradius = arrayhilfsebene1[indices[0][0]][5] / (hrber2 * (1 + veinflussradius))
                    loesungspannradius = arrayhilfsebene1[indices[0][0]][6] / (hrber2 * (1 + seinflussradius))

            #Für abweichende Breite
            hb = arrayhilfsebene1[indices[0][0]][1] * 10
            hb1 = normedinput[0][1] * 10
            hbber = (0.0224 * hb) ** (-0.001)
            hbber1 = (0.0224 * hb1) ** (-0.001)
            hbber2 = hbber / hbber1

            if hbber2 > 1:
                loesungverfbreite = loesungverfradius / (hbber2 * (1 + veinflussbreite))
                loesungspannbreite = loesungspannradius / (hbber2 * (1 + seinflussbreite))
            else: 
                if hbber2 == 1:
                    loesungverfbreite = loesungverfradius
                    loesungspannbreite = loesungspannradius
                else:
                    loesungverfbreite = loesungverfradius / (hbber2 * (1 + veinflussbreite))
                    loesungspannbreite = loesungspannradius / (hbber2 * (1 + seinflussbreite))


            #Für abweichende Dicke funktioniert
            hd = arrayhilfsebene1[indices[0][0]][2] * 10
            hd1 = normedinput[0][2] * 10
            hdber = (3.0832 * hd) ** (-3.051)
            hdber1 = (3.0832 * hd1) ** (-3.051)
            hdber2 = hdber / hdber1

            if hdber2 > 1:
                loesungverfdicke = loesungverfbreite / (hdber2 * (1 + veinflussdicke))
                loesungspanndicke = loesungspannbreite / (hdber2 * (1 + seinflussdicke))
            else: 
                if hdber2 == 1:
                    loesungverfdicke = loesungverfbreite
                    loesungspanndicke = loesungspannbreite
                else:
                    loesungverfdicke = loesungverfbreite / (hdber2 * (1 + veinflussdicke))
                    loesungspanndicke = loesungspannbreite / (hdber2 * (1 + seinflussdicke))

            #Für abweichende Länge

            hl = arrayhilfsebene1[indices[0][0]][3] * 10
            hl1 = normedinput[0][3] * 10
            hlber = (0.0246 * hb) ** (-0.165)
            hlber1 = (0.0246 * hb1) ** (-0.165)
            hlber2 = hlber / hlber1

            if hlber2 > 1:
                loesungverflaenge = loesungverfdicke / (hbber2 * (1 + veinflusslaenge))
                loesungspannlaenge = loesungspanndicke / (hbber2 * (1 + seinflusslaenge))
            else: 
                if hlber2 == 1:
                    loesungverflaenge = loesungverfdicke
                    loesungspannlaenge = loesungspanndicke
                else:
                    loesungverflaenge = loesungverfdicke / (hbber2 * (1 + veinflusslaenge))
                    loesungspannlaenge = loesungspanndicke / (hbber2 * (1 + seinflusslaenge))


            #Für abweichende Kraft funktioniert
            hilfkraft = arrayhilfsebene1[indices[0][0]][4] / normedinput[0][4]
            #<> gewechselt
            if hilfkraft < 1:
                loesungverfkraft = loesungverflaenge /   (hilfkraft  * (1 + veinflusskraft))
                loesungspannkraft = loesungspannlaenge /  (hilfkraft  * (1 + seinflusskraft))
            else: 
                if hilfkraft == 1:
                    loesungverfkraft = loesungverflaenge
                    loesungspannkraft = loesungspannlaenge
                else:
                    loesungverfkraft = loesungverflaenge /   (hilfkraft  * (1 + veinflusskraft))
                    loesungspannkraft = loesungspannlaenge /  (hilfkraft  * (1 + seinflusskraft))

            print ('radius')
            print(loesungverfradius)
            print(loesungspannradius)
            print ('breite')
            print(loesungverfbreite)
            print(loesungspannbreite)
            print ('dicke')
            print(loesungverfdicke)
            print(loesungspanndicke)
            print ('laenge')
            print(loesungverflaenge)
            print(loesungspannlaenge)
            print ('kraft')
            print(loesungverfkraft)
            print(loesungspannkraft)

            # Ergebnisse anzeigen
            # re.sub() wird genutzt um manche Ergebnisse ohne Klammern anzuzeigen
            fenster['-Ergebnis-Aehnlich-'].update(re.sub('[\[\]]', '', np.array2string(arrayzerlegt1[indices])))
            fenster['-Ergebnis-Vergleichspannung-'].update(re.sub('[\[\]]', '', np.array2string(arrayloesung5[indices])))
            fenster['-Ergebnis-Verschiebung-'].update(re.sub('[\[\]]', '', np.array2string(arrayloesung6[indices])))
            fenster['-Ergebnis-Distanz-'].update(re.sub('[\[\]]', '', np.array2string(distances)))
            fenster['-Ergebnis-Index-'].update(re.sub('[\[\]]', '', np.array2string(indices)))
            fenster['-Ergebnis-Perzentil-'].update(percentsolution)
            fenster['-Ergebnis-Verformung-'].update(str(loesungverfkraft))
            fenster['-Ergebnis-Spannung-'].update(str(loesungspannkraft))

        fenster.refresh()

# Wird gebraucht um main zu starten 
if __name__ == "__main__":
    main()