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
    

def parse_verwendungszweck(row, description):
    return description\
        .replace("{Vorname}", row["Vorname"])\
        .replace("{Nachname}", row["Nachname"])

def is_today(date: datetime.datetime):
    return date.date() == datetime.date.today()

