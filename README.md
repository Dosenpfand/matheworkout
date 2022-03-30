# Mathe-Matura-Quiz

## Run it:

```
export FLASK_APP=app/__init__.py
export FLASK_ENV=development
flask fab create-admin
flask run
```

## TODO
- [ ] User Statisiken (Anzahl Fragen gesamt (inklusive Gruppen), Anzahl richtig, Reset, oder: extra Tabelle tries mit ref zu user und question?)
- [ ] Auswahl spezifische Ausgabe aus einer Liste, oder aus Topic
- [ ] User Gruppen (Klassen), Überblick über Ergebnisse für Lehrer
- [ ] Schüler: Typ (2 aus 5, etc.) Random, Inhaltsgebiet (Algebra 1, Algebra 2, etc.) auswählbar (z.B. Schüler wählt aus Inhaltsgebiet "Wahrscheinlichkeitsrechnung" und Typ)
- [ ] User Registierung: Rechte-Vergabe, Views, etc.
- [ ] DB migration
- [ ] View multiple tables: `CREATE VIEW alle3 as SELECT external_id, topic_id, 'a' FROM question1of6 UNION SELECT external_id, topic_id, 'b' FROM question2of5`
