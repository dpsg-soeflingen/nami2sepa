import pandas as pd


def calc_beitrag(df):
    # Standard beitrag calculation
    df["Beitrag"] = df.apply(lambda row: calc_base_beitrag(row), axis=1)
    # Manual Beitrag override
    df["Beitrag"] = df["OverrideBeitrag"].fillna(df["Beitrag"])
    # Aktions-Beitrag
    df["Beitrag"] = df["AktionBeitrag"].fillna(df["Beitrag"])
    return df


def calc_base_beitrag(row):
    """
    Calculate fees of a certain member.
    Leiter/Vorstaende: 15 Eur
    Familienermaessigt: 20 Eur
    Voller Beitrag: 27.50 Eur
    """
    beitrag = row["BeitragArt"]
    if row["Leader/CEO"] == True:
        return 15
    if "Sozialermäßigt" in beitrag:
        return -1
    if "Familienermäßigt" in beitrag:
        return 20
    if "Voller Beitrag" in beitrag:
        return 27.50
    if "Sozialtopf" in beitrag:
        return 10


# Determine Leiter.
def determine_leiter(tasks_file_path):
    """
    Definition Leiter:
    - Is an active member (did not resign).
    - Has a current task (not yet finished) as a Leiter (Taetigkeit == "€ LeiterIn")
    - OR: Is Stammesvorstand (Stufe_Abteilung == "Vorstand")
    """
    tasks = pd.read_excel(tasks_file_path)
    leader_ids = tasks.loc[(tasks["Status"] == "AKTIV")\
            & (tasks["Aktiv_Bis"] == "-null-")\
            & ((tasks["Taetigkeit"] == "€ LeiterIn") | (tasks["Stufe_Abteilung"] == "Vorstand"))\
        ].groupby("Mitgliedsnummer").head(1)["Mitgliedsnummer"]
    return leader_ids
