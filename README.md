# Mathe-Matura-Quiz

## Run it:

```
export FLASK_APP=app/__init__.py
export FLASK_ENV=development
flask fab create-admin
flask run
```

## TODO
- [ ] User Statistiken (Anzahl Fragen gesamt (inklusive Gruppen), Anzahl richtig, Reset, oder: extra Tabelle tries mit ref zu user und question?)
- [ ] Auswahl spezifische Ausgabe aus einer Liste, oder aus Topic
- [ ] User Gruppen (Klassen), Überblick über Ergebnisse für Lehrer
- [ ] Schüler: Typ (2 aus 5, etc.) Random, Inhaltsgebiet (Algebra 1, Algebra 2, etc.) auswählbar (z.B. Schüler wählt aus Inhaltsgebiet "Wahrscheinlichkeitsrechnung" und Typ)
- [ ] DB migration
- [ ] Detailed user statistics: Which questions correct/incorrect answered -> repeat incorrect, statistic per topic
- [ ] Selbstkontrolle: Nächste Aufgabe gibt immer random
- [ ] lehrer kann aufgabensammlung (set an aufgaben) zusammenstellen und sie klassen (schülern) zuweisen, und ergebnisse kontrollieren
