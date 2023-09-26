from dataclasses import dataclass
from datetime import datetime

import pandas as pd


@dataclass
class SepaInformations:
    vorname: str
    nachname: str
    kontoinhaber_vorname: str
    kontoinhaber_nachname: str
    bic: str
    iban: str
    mandat: str
    verwendungszweck: str
    is_first_payment: bool
    sepa_datum: datetime
    betrag: float
    end2end_id: str
    is_leader: bool = False


def get_leader_state(user, nami):
    activities = nami.mgl_activities(user.id)
    current_activities = [act.taetigkeit for act in activities if not act.aktivBis]
    print(current_activities)
    return any([("LeiterIn" in act) for act in current_activities])


def calc_betrag(user, betrag, override_betrag, is_leader):
    # TODO Make Beitragsarten configurable.
    if betrag is not None:
        return betrag
    elif not pd.isna(override_betrag):
        return override_betrag
    elif is_leader:
        return 15
    elif "Sozialermäßigt" in user.beitragsart:
        return -1
    elif "Familienermäßigt" in user.beitragsart:
        return 22.5
    elif "Voller Beitrag" in user.beitragsart:
        return 27.5
    else:
        print(f"Error in calc_betrag()! {user.vorname} {user.nachname}")
        return 0


def gather_information(vorname, nachname, betrag, verwendungszweck, project_data, nami, sepa_info):
    vorname, nachname = vorname.strip(), nachname.strip()
    search_result = nami.search(vorname=vorname, nachname=nachname)
    assert_unique_search_result(search_result, vorname, nachname)
    user = search_result[0].get_mitglied(nami)

    # Nami Information
    kontoinhaber_vorname, kontoinhaber_nachname = user.kontoverbindung.kontoinhaber.rsplit(" ", 1)
    bic = user.kontoverbindung.bic
    iban = user.kontoverbindung.iban
    mandat = user.mitgliedsNummer

    # Project Data
    verwendungszweck = verwendungszweck.strip() + f" {vorname} {nachname}"
    end2end_id = project_data.iloc[0].End2EndId.strip()
    is_leader = pd.isnull(project_data.iloc[0].Vorname) and get_leader_state(user, nami)

    # Users Sepa Information
    user_sepa_info = sepa_info.loc[mandat]
    is_first_payment = pd.isnull(user_sepa_info.Erstlastschrift)
    sepa_datum = user_sepa_info.Datum
    betrag = calc_betrag(user, betrag, user_sepa_info.OverrideBeitrag, is_leader)
    return SepaInformations(
        vorname=vorname,
        nachname=nachname,
        kontoinhaber_vorname=kontoinhaber_vorname,
        kontoinhaber_nachname=kontoinhaber_nachname,
        bic=bic,
        iban=iban,
        mandat=mandat,
        verwendungszweck=verwendungszweck,
        is_first_payment=is_first_payment,
        sepa_datum=sepa_datum,
        betrag=betrag,
        end2end_id=end2end_id,
        is_leader=is_leader,
    )


def assert_unique_search_result(search_result, vorname, nachname):
    if len(search_result) == 0:
        print(f"No result found matching {vorname} {nachname}. Exiting.")
    elif len(search_result) > 1:
        print(f"{len(search_result)} results found matching {vorname} {nachname}. Exiting.")
    else:
        return
    exit()

