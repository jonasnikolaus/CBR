# README für Case-Based Reasoning Tool

## Überblick

Das Case-Based Reasoning Tool ist eine Python-Anwendung, die eine benutzerfreundliche Schnittstelle bietet, um ähnliche Fälle basierend auf spezifischen Eingabeparametern zu finden und zu analysieren. Das Tool nutzt maschinelles Lernen und statistische Methoden, um Vorhersagen und Vergleiche mit bestehenden Datensätzen zu ermöglichen.

## Features

- **Eingabe von Parametern**: Benutzer können verschiedene Parameter wie Länge, Dicke, Breite, Radius und Kraft angeben.
- **Berechnung und Analyse**: Das Tool berechnet die ähnlichsten Fälle basierend auf den eingegebenen Parametern und zeigt relevante Ergebnisse an, wie z.B. Vergleichsspannung, Verschiebung und die Distanz zum nächstliegenden Fall.
- **Statistische Auswertungen**: Es werden Perzentile zur Bewertung der Nähe der Fälle angegeben.
- **Lineare Regression**: Das Tool verwendet lineare Regression, um Vorhersagen über Verformung und Spannung zu machen.
- **Benutzerfreundliche Oberfläche**: Eine einfache und intuitive Benutzeroberfläche, die mit PySimpleGUI erstellt wurde.

## Technische Details

- **Python-Bibliotheken**: scikit-learn, numpy, PySimpleGUI
- **Datenauswertung und -verarbeitung**: Der Code liest Daten aus einer CSV-Datei, verarbeitet diese und führt Berechnungen durch, um ähnliche Fälle zu finden.
- **Normierung und Linear Regression**: Die Anwendung normiert die Eingabedaten und wendet lineare Regressionsmodelle an.

## Installation

1. Stellen Sie sicher, dass Python auf Ihrem System installiert ist.
2. Installieren Sie die erforderlichen Bibliotheken:

pip install numpy scikit-learn PySimpleGUI


3. Klonen Sie das Repository oder laden Sie die Code-Dateien herunter.
4. Führen Sie das Skript über eine Python-IDE oder das Terminal aus.

## Benutzung

1. Starten Sie das Programm.
2. Geben Sie die gewünschten Parameter in die vorgesehenen Felder ein.
3. Klicken Sie auf "Berechnen", um die Analyse zu starten.
4. Die Ergebnisse werden in der Benutzeroberfläche angezeigt.

## Beitrag

Ihr Beitrag zu diesem Projekt ist willkommen.
