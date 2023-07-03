#!/usr/bin/env python3

from nami2sepa import main

import os
from argparse import ArgumentParser
import warnings
warnings.filterwarnings("ignore")

def parse_arguments():
    parser = ArgumentParser(prog="SEPA Creator", description="Erstellt eine csv-Datei fuer SEPA-Sammeleinzuege aus Daten aus dem NaMi.\
    Gib in die Nami-Suche 'Beitragsart und Kontoverbindung' ein und uebergib das File unter der Option '-p'. In der Nami-Suche unter 'Mitglieder: Grundinformationen mit Taetigkeiten und Stufe Abteilung' wird ein File gedownloadet, das man unter der Option '-t' angeben muss. \
    Des Weiteren gibt es das File Sepa_Informations.xlsx, das Mandatsdatum, Ersteinzugsdatum, manuellen Beitrag etc. angibt.")
    parser.add_argument("-a", "--accounts_file", help="Pfad zur Excel-Datei, in der NaMi-Suche: 'Beitragsart und Kontoverbindung.'")
    parser.add_argument("-t", "--tasks_file", help="Pfad zur Excel-Datei, in der NaMi-Suche: 'Mitglieder: Grundinformationen mit Taetigkeiten und Stufe Abteilung'.")
    parser.add_argument("-p", "--project_file", help="Pfad zur Excel-Datei, die Mitgliedsnummer und Betrag fuer eine Aktion angibt.")
    parser.add_argument("-o", "--output", default="output.xml", help="Pfad zur Output-Datei, die der Bank fuer den Sammel-Einzug gegeben werden kann.")
    args = parser.parse_args()
    for argument, value in vars(args).items():
        if value is not None:
            setattr(args, argument, os.path.abspath(value))
    return args


def run():
    args = parse_arguments()
    main.run(**vars(args))
    
