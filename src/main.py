#!/bin/env python

import logic, parsing, utils, xml_convert

import warnings
warnings.filterwarnings('ignore')


def run(accounts_file, tasks_file, project_file, output, scan_dir):
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

    # TODO Activate/Deactivate in config!
    # TODO Incorrect! Can be overwritten by manual setting in e.g. Aktionen!
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
    output_xml(sepa, output)


def output_xml(df, file_path):
    with open(file_path, "w") as out_file:
        out_file.write(xml_convert.generate_xml(df))


