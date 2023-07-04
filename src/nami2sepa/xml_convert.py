#!/bin/env python

from nami2sepa import utils

from sepaxml import SepaDD
import datetime
import json
import pandas as pd
import os
import logging


def generate_xml(orders):
    with open(os.path.expanduser("~/.config/nami2sepa/sepa_config.json"), "r") as file:
        config = json.load(file)

    sepa_rcur = SepaDD(config, schema="pain.008.001.02", clean=True)
    sepa_frst = SepaDD(config, schema="pain.008.001.02", clean=True)

    has_rcur, has_frst = False, False

    for _, order in orders.iterrows():
        if pd.isna(order).sum():
            logging.error(f"FEHLERHAFTE DATEN: {order.Mandat} {order.Verwendungszweck}")
            continue
        is_first_payment = utils.is_today(order.Erstlastschrift)
        payment = {
            "name": f"{order.Name}, {order.Vorname}",
            "IBAN": order.IBAN,
            "BIC": order.BIC,
            "amount": int(round(float(order.Beitrag)*100)),
            "type": "FRST" if is_first_payment else "RCUR",
            "collection_date": datetime.date.today(),
            "mandate_id": str(order.Mandat),
            "mandate_date": order.Mandatsdatum,
            "description": order.Verwendungszweck,
            "endtoend_id": order.Identifikation,
        }
        if is_first_payment:
            has_frst = True
            # TODO Update Sepa_Informations.xlsx.
            logging.info(f"Erstlastschrift {order.Verwendungszweck}")
            sepa_frst.add_payment(payment)
        else:
            has_rcur = True
            sepa_rcur.add_payment(payment)
    sepa_rcur_output = sepa_rcur.export().decode("utf-8") if has_rcur else None
    sepa_frst_output = sepa_frst.export().decode("utf-8") if has_frst else None
    return sepa_rcur_output, sepa_frst_output
