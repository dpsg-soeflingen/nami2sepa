# NaMi2SEPA

NaMi2SEPA ermoeglicht einfaches Generieren von SEPA-Lastschriften direkt aus der DPSG Mitgliederverwaltung NaMi.
Wichtige Informationen sind in Konfigurations-Dateien ausgelagert, die einfach angepasst werden koennen.

## Installation
Klone das Repository und installiere NaMi2SEPA durch pip:
````shell
git clone 'git+https://github.com/dpsg-soeflingen/nami2sepa.git'
cd nami2sepa
pip install .
````

Die Deinstallation erfolgt mit dem folgenden Befehl:
````shell
pip uninstall nami2sepa
````

## Vereinsspezifische Konfiguration
Lege die Dateien unter ``config/`` auf deinem lokalen Computer unter ``.config/nami2sepa/`` ab.
Erstelle das Verzeichnis, wenn es noch nicht vorhanden ist. \
Fuelle die ``sepa_config.toml`` mit den SEPA-Informationen deines Vereins.
Des Weiteren ist in demselben Ordner eine ``Sepa_Informations.xlsx``.
Da die Bank das Datum der Erstlastschrift sowie der SEPA-Unterschrift benoetigt und diese Informationen nicht im NaMi hinterlegbar sind, muss diese Liste manuell gefuehrt werden.

## Nutzung
Als Grundlage zur Nutzung wird eine Excel-Datei verwendet, die jedem Benutzer einen einzuziehenden Betrag zuweist.
Ein Beispiel zu einer solchen Datei ist unter ``lib/InputTemplate.xlsx`` zu finden.
Starte das Tool in einem Verzeichnis mit genau einer solchen Input-Datei.
Dieses wird automatisch erkannt.
````shell
nami2sepa
````
Alle weiteren Kommandozeilen-Argumente koennen in der Hilfe nachgelesen werden: ``nami2sepa -h``.

## Die Input-Datei

Diese Excel-Datei beinhaltet die Aktions-spezifischen Informationen:

- Vorname, Nachname: Angaben, die eindeutig sein und mit NaMi uebereinstimmen muessen.
- Betrag: Der jeweils zu zahlende Betrag pro Teilnehmer.
- Verwendungsweck: Der Verwendungszweck, den jeder SEPA-Lastschrift haben wird. Diesem wird mit der jeweilige Vor- und Nachname angehaengt.
- End2EndId: Eine ID, die diesen Sammeleinzug eindeutig bestimt. Zum Beispiel "sola23" fuer das Sommerlager 2023.

Werden keine einzelnen Teilnehmer durch Vor-, Nachname und Betrag aufgelistet, wird eine Sammellastschrift fuer alle Teilnehmer erstellt, wobei je nach Position (Mitglied oder Leiter) und Beitragsart (Voller Betrag, Familienbeguenstigt, Reduzierter Betrag) der Betrag ermittelt wird.

## Automatische Beitrags-Berechnung

Da in NaMi die Taetigkeiten der einzelnen Mitglieder protokolliert sind, werden folgende Beitragsstufen unterschieden:
- Sozialtopf (werden vom Einzug ignoriert und die betroffenen Mitglieder-Identifikationen ausgegeben. Dies muss auf manuellem Weg erfolgen.)
- Mitglied (Voller Beitrag)
- Mitglied (Familien Beitrag)
- Leiter
- Alumni/Aktive Mitglieder (Manuell in ``~/.config/nami2sepa/Sepa_Informations.xlsx`` gefuehrt.)

## Automatisches Erstellen von Projekt-Einzuegen

[WIP] \
Der folgende Befehl soll einen Ordner mit zugehoerigen files erstellen:
````shell
nami2sepa new <aktionsname>
````
