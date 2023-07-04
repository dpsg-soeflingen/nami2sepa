#!/bin/env python

from nami2sepa import (
    logic,
    parsing,
    utils,
    xml_convert
)

import logging
import os
import warnings
warnings.filterwarnings('ignore')


def _make_absolute(path):
    if path is not None:
        return os.path.join(os.getcwd(), path)
    return None

def run(accounts_file, tasks_file, project_file, output):
    scan_dir = os.getcwd()
    accounts_file = _make_absolute(accounts_file)
    tasks_file = _make_absolute(tasks_file)
    project_file = _make_absolute(project_file)
    output = _make_absolute(output)
    sepa_infos = "~/.config/nami2sepa/Sepa_Informations.xlsx"
    if any([elem is None for elem in [accounts_file, tasks_file, project_file]]):
        inferred_file_names = utils.infer_file_names(
            scan_dir,
            accounts=accounts_file, 
            tasks=tasks_file,
            project=project_file
        )
        accounts_file = inferred_file_names["accounts"]
        tasks_file = inferred_file_names["tasks"]
        project_file = inferred_file_names["project"]
    leiter_ids = logic.determine_leiter(tasks_file)
    accounts_info = parsing.parse_account_information(accounts_file, leiter_ids)
    sepa_info = parsing.parse_external_sepa_information(sepa_infos)
    project_data = parsing.parse_project_information(project_file, accounts_info)
    data = utils.join(accounts_info, sepa_info)
    data = utils.join(data, project_data)
    data = data.loc[data["Mandat"].isin(project_data.index)]
    data = logic.calc_beitrag(data)

    # TODO Incorrect! Can be overwritten by manual setting in e.g. Aktionen!
    # Should be called "ignore-members"
    # Remove members within Sozialtopf.
    ignored_members = data[data["Beitrag"] < 0]
    if len(ignored_members) > 0:
        for _, ignored_member in ignored_members.iterrows():
            logging.warning(f"Ignoriere {ignored_member.Verwendungszweck}.")
    data = data.drop(ignored_members.index)

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
    output_xml(sepa, output)


def output_xml(df, file_path):
    with open(file_path, "w") as out_file:
        out_file.write(xml_convert.generate_xml(df))

def new(project_name):
    curr_dir = os.getcwd()
    os.mkdir(os.path.join(curr_dir, project_name))
