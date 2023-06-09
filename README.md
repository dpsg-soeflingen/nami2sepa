# NaMi2SEPA

NaMi2SEPA ermoeglicht einfaches Generieren von SEPA-Lastschriften aus NaMi-Exports.
Wichtige Informationen sind in Konfigurations-Dateien ausgelagert, die einfach angepasst werden koennen.

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
Konfiguriere die Berechnung von Beitraegen in der ``project_config.json``.

## Nutzung
Exportiere die Files ``Mitglieder: Grundinformationen mit Taetigkeiten und Stufe Abteilung`` und ``Beitragsart und Kontoverbindung`` aus dem NaMi:

![Taetigkeiten](images/Taetigkeiten_Export.png)
![Kontoverbindungen](images/Grundinfos_Export.png)

Starte nun das Tool mit den folgenden Parametern:
````shell
sepa_creator -a <Pfad zur Kontoverbindungs-Datei> -t <Pfad zur Taetigkeiten-Datei> -i <Pfad zur SEPA-Informations Datei (nicht aus NaMi)> -p <Pfad zur Aktions-Datei>
````
Alle weiteren Kommandozeilen-Argumente koennen in der Hilfe nachlegesen werden: ``sepa_creator -h``.

## Die Aktions-Datei

Diese Datei 
