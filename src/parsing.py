import parsing

import pandas as pd
import json
import functools
import datetime


def parse_verwendungszweck(row, description):
    return description\
        .replace("{Vorname}", row["Vorname"])\
        .replace("{Nachname}", row["Nachname"])


# Parse account information.
# [Only needs group-file]
def parse_account_information(accounts_file_path, leader_ids):
    group = pd.read_excel(accounts_file_path)
    group.index = group["Mitgliedsnummer"]
    group = group.loc[group["Status"] == "Aktiv"]

    group.loc[leader_ids, "Leader/CEO"] = True
    group["Leader/CEO"] = group["Leader/CEO"].fillna(False)

    sepa = group[["Vorname", "Nachname", "Mitgliedsnummer", "IBAN", "BIC", "BeitragArt", "Kontoinhaber", "Leader/CEO"]]
    # Get payer name.
    sepa[["Zahler_Vorname", "Zahler_Name"]] = sepa["Kontoinhaber"].str.rsplit(" ", n=1, expand=True)
    # Get payment-identification.
    sepa = sepa.rename({"Mitgliedsnummer": "Mandat"}, axis=1)
    return sepa


# Parse SEPA-Information not saved within NaMi.
def parse_external_sepa_information(sepa_information_file_path):
    sepa_information = pd.read_excel(sepa_information_file_path)
    sepa_dates = pd.DataFrame()
    sepa_dates["Mandat"] = sepa_information["Mitgliedsnummer"]
    sepa_dates["Mandatsdatum"] = sepa_information["Datum"].map(lambda e: e.date())
    # If this is the first Einzug, fill-in today's date.
    sepa_dates["Erstlastschrift"] = sepa_information["Erstlastschrift"].fillna(datetime.datetime.now())
    sepa_dates["Letztlastschrift"] = ""
    sepa_dates["OverrideBeitrag"] = sepa_information["OverrideBeitrag"]
    return sepa_dates


# PROJECT-SPECIFIC PARSING!
def parse_project_information(project_file_path, base_data):
    with open(project_file_path, "r") as project_file:
        project_information = json.load(project_file)
    fee_info = pd.DataFrame.from_dict(project_information["Beitragsinformationen"], orient="index", columns=["Beitrag"])
    if len(fee_info) > 0:
        project_data = base_data.loc[base_data["Mandat"].astype(str).isin(fee_info.index)][["Mandat", "Vorname", "Nachname", "BeitragArt", "Leader/CEO"]]
    else:
        project_data = base_data[["Mandat", "Vorname", "Nachname", "BeitragArt", "Leader/CEO"]]
    # Insert Verwendungszweck.
    project_data["Verwendungszweck"] = project_data.apply(functools.partial(parsing.parse_verwendungszweck, description=project_information["Verwendungszweck"]), axis=1)
    project_data["Identifikation"] = project_information["end2end-id"]

    # Calculate Beitrag
    fee_info.index = fee_info.index.astype(int)
    project_data["AktionBeitrag"] = fee_info["Beitrag"]

    return project_data[["Mandat", "AktionBeitrag", "Verwendungszweck", "Identifikation"]]
