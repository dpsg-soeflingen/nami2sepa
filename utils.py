import datetime

def calc_beitrag(row):
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
    

def gen_usage(row, half, year):
    """
    Generate Verwendungszweck.
    """
    firstname = row["Vorname"]
    lastname = row["Nachname"]
    return f"DPSG Ulm-Soeflingen Mitgliederbeitrag {half}. Halbjahr {year} fuer {lastname} {firstname}"


def is_today(date: datetime.datetime):
    return date.date() == datetime.date.today()

