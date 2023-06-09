# NaMi2SEPA

NaMi2SEPA ist ein Tool mit dem man einfach SEPA-Lastschriften aus NaMi-Exports generieren lassen kann.
Hauptkomponenten sind durch eine Konfigurations-Datei einstellbar.

## Installation
Fuehre den folgenden Befehl aus, um das Tool zu installieren:
````shell
make
````

Die Deinstallation erfolgt mit dem folgenden Befehl:
````shell
make uninstall
````

## Vereinsspezifische Konfiguration
Fuelle die ``sepa_config.json`` mit den SEPA-Informationen deines Vereins aus. \
Konfiguriere die Berechnung von Beitraegen in der ``config.json``.

## Nutzung
Exportiere 


Todos:
- 2 Files generated from NaMi
- One File for Sepa Mandate, override fees, ...
- One Project-File. Should include actual fees if not normal annual and participants (Mitgliedernummern).

Create project: 
- Get up-to-date files from NaMi.
- Use SEPA-info file (static in this case)
- Provide project file.
- Run script

Problem:
- I want to automate the "Getting files from NaMi"-part ...

But first, implement the project file!

Should be Aktions file.
