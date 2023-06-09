#!/bin/env python

import utils

from sepaxml import SepaDD
import datetime, uuid
import json
import pandas as pd


def generate_xml(orders):
    with open("./sepa_config.json", "r") as file:
        config = json.load(file)

    sepa = SepaDD(config, schema="pain.008.001.02", clean=True)

    for _, order in orders.iterrows():
        if pd.isna(order).sum():
            print("FEHLERHAFTE DATEN:", order.Mandat, order.Verwendungszweck)
            continue
        payment = {
            "name": f"{order.Name}, {order.Vorname}",
            "IBAN": order.IBAN,
            "BIC": order.BIC,
            "amount": int(float(order.Beitrag)*100),
            "type": "FRST" if utils.is_today(order.Erstlastschrift) else "RCUR",
            "collection_date": datetime.date.today(),
            "mandate_id": str(order.Mandat),
            "mandate_date": order.Mandatsdatum,
            "description": order.Verwendungszweck,
            "endtoend_id": order.Identifikation,
        }

        sepa.add_payment(payment)
    return sepa.export().decode("utf-8")
