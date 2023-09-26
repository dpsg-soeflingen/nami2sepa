#!/usr/bin/env python3

from nami2sepa import main

from argparse import ArgumentParser
import warnings
warnings.filterwarnings("ignore")

def parse_arguments():
    parser = ArgumentParser(prog="SEPA Creator", description="Erstellt eine csv-Datei fuer SEPA-Sammeleinzuege aus Daten aus dem NaMi.\
    Des Weiteren gibt es das File Sepa_Informations.xlsx, das Mandatsdatum, Ersteinzugsdatum, manuellen Beitrag etc. angibt.")
    parser.add_argument("-p", "--project_path", help="Pfad zur Excel-Datei, die Mitgliedsnummer und Betrag fuer eine Aktion angibt.")
    parser.add_argument("-o", "--output_path", default="output.xml", help="Pfad zur Output-Datei, die der Bank fuer den Sammel-Einzug gegeben werden kann.")

    subparsers = parser.add_subparsers(dest="subcommand")

    parser_new = subparsers.add_parser("new", help="Erstellt eine neue Sammellastschrift.")
    parser_new.add_argument("project_name", help="Name der Aktion/des Sammeleinzugs.")
    args = parser.parse_args()
    #for argument, value in vars(args).items():
    #    if value is not None:
    #        setattr(args, argument, os.path.abspath(value))
    return args


def run():
    args = parse_arguments()
    if args.subcommand == "new":
        main.new(args.project_name)
    else:
        main.run(
            project_path=args.project_path,
            output_path=args.output_path
        )
    
