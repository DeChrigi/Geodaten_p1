Anbei noch eine Erläuterung zu den einzelnen Files und ein paar zusätzliche Informationen.

Das Scraping der ÖV, Schul und Krankenhäuserdaten wurden über folgende Pythonfiles umgesetzt:
- dataretrieval_hospitals.py
- dataretrieval_oev.py
- dataretrieval_schools.py

Die Daten werden danach mit dem Python Script bzw. der Klasse
- DBHandler.py
in die Postgresdatenbank geschrieben.

Die Tabellen in der Postgres-DB haben dann die Namen:
- oev_raw
- schools_raw
- hospitals_raw

Die gespeicherten Datensätze werden danach mit dem Python Script
- etl_pypeline.py
aus der Datenbank gelesen und die Adressen geocodiert. 

Danach werden die Daten wieder in die Datenbank gespeichert mit den folgenden Namen:
- oev_transformed
- schools_transformed
- hospitals_transformed

Die Longitude und Latitude Werte in den Tabellen werden danach in Postgres in den geom Datentyp umgewandelt und in materialized Views gespeichert, um diese in QGIS zu verwenden.

Die Adressen werden danach noch Kanton Zürich gefiltert mittels den PLZ im dem 'Liste-der-PLZ-in-excel-Karte-Schweiz-Postleitzahlen.csv'

Die Datei qgis teil.qgz berechnet die Isochronen und speichert diese wiederum zurück in die Postgres Datenbank mit den Namen:

- hospitals_final_zh_isochrones_v2
- schools_final_zh_isochrones_v2

Danach werden die Anzahl ÖV-Stationen in den Isochronen berechnet in der Datei
- gis_calculations.py
und wieder zurück in die Postgres gespeichert.

Schlussendlich werden die Daten im Frontend visualisiert mit einer Karte und Tabelle. Zusätzlich wurde eine Tableau Arbeitsmappe erstellt um die Resultate genauer auszuwerten
