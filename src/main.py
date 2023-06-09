#!/bin/env python

import logic, parsing, utils, xml_convert

from argparse import ArgumentParser
import warnings
warnings.filterwarnings('ignore')


def parse_arguments():
    parser = ArgumentParser(prog="SEPA Creator", description="Erstellt eine csv-Datei fuer SEPA-Sammeleinzuege aus Daten aus dem NaMi.\
    Gib in die Nami-Suche 'Beitragsart und Kontoverbindung' ein und uebergib das File unter der Option '-p'. In der Nami-Suche unter 'Mitglieder: Grundinformationen mit Taetigkeiten und Stufe Abteilung' wird ein File gedownloadet, das man unter der Option '-t' angeben muss. \
    Des Weiteren gibt es das File Sepa_Informations.xlsx, das Mandatsdatum, Ersteinzugsdatum, manuellen Beitrag etc. angibt.")
    parser.add_argument("-a", "--accounts_file", help="Pfad zur Excel-Datei, in der NaMi-Suche: 'Beitragsart und Kontoverbindung.'", required=True)
    parser.add_argument("-t", "--tasks_file", help="Pfad zur Excel-Datei, in der NaMi-Suche: 'Mitglieder: Grundinformationen mit Taetigkeiten und Stufe Abteilung'.", required=True)
    parser.add_argument("-i", "--sepa_infos", default="Sepa_Informations.xlsx", help="Pfad zur Excel-Datei, um SEPA-Infos zu erhalten, die nicht im NaMi gespeichert sind.")
    parser.add_argument("-p", "--project_file", help="Pfad zur Excel-Datei, die Mitgliedsnummer und Betrag fuer eine Aktion angibt.")
    parser.add_argument("-o", "--output", default="output.xml", help="Pfad zur Output-Datei, die der Bank fuer den Sammel-Einzug gegeben werden kann.")
    return  parser.parse_args()


def run(args):
    leiter_ids = logic.determine_leiter(args.tasks_file)
    accounts_info = parsing.parse_account_information(args.accounts_file, leiter_ids)
    sepa_info = parsing.parse_external_sepa_information(args.sepa_infos)
    project_data = parsing.parse_project_information(args.project_file, accounts_info)
    data = utils.join(accounts_info, sepa_info)
    data = utils.join(data, project_data)
    data = data.loc[data["Mandat"].isin(project_data.index)]
    data = logic.calc_beitrag(data)

    # TODO Activate/Deactivate in config!
    # Should be called "ignore-members"
    # Remove members within Sozialtopf.
    # sepa = sepa[sepa["Beitrag"] > 0]

    # Sort columns.
    data = data \
        .drop(["BeitragArt", "Leader/CEO", "Vorname", "Nachname", "Kontoinhaber"], axis=1) \
        .rename({"Zahler_Vorname": "Vorname", "Zahler_Name": "Name"}, axis=1) \
        .reset_index() \
        .drop("Mitgliedsnummer", axis=1)
    data.index.name = "Nummer"
    data.index += 1
    # sort columns
    sepa  = data[["Name", "Vorname", "Identifikation", "BIC", "IBAN", "Mandat", "Mandatsdatum", "Erstlastschrift", "Letztlastschrift", "Beitrag", "Verwendungszweck"]]
    output_xml(sepa, args.output)


def output_xml(df, file_path):
    with open(file_path, "w") as out_file:
        out_file.write(xml_convert.generate_xml(df))


if __name__ == "__main__":
    args = parse_arguments()
    run(args)


