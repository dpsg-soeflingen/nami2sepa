#!/bin/env python

import datetime
import os
import tomllib
from dataclasses import astuple

import pandas as pd
from loguru import logger
from sepaxml import SepaDD


def generate_xml(orders):
    with open(os.path.expanduser("~/.config/nami2sepa/sepa_config.toml"), "rb") as file:
        config = tomllib.load(file)["sepa"]

    sepa_config = config | {"batch": True}
    # pain.008 is the correct format for direct debit.
    sepa_rcur = SepaDD(sepa_config, schema="pain.008.001.02", clean=True)
    sepa_frst = SepaDD(sepa_config, schema="pain.008.001.02", clean=True)

    has_rcur, has_frst = False, False

    for order in orders:
        if any([pd.isnull(o) for o in astuple(order)]):
            logger.error(
                f"FEHLERHAFTE DATEN: {order.mandat} {order.verwendungszweck}. Wird uebersprungen."
            )
            continue
        payment = {
            "name": f"{order.kontoinhaber_nachname}, {order.kontoinhaber_vorname}",
            "IBAN": order.iban,
            "BIC": order.bic,
            "amount": int(round(float(order.betrag) * 100)),
            "type": "FRST" if order.is_first_payment else "RCUR",
            "collection_date": datetime.date.today(),
            "mandate_id": str(order.mandat),
            "mandate_date": order.sepa_datum.date(),
            "description": order.verwendungszweck,
            "endtoend_id": order.end2end_id,
        }
        if order.is_first_payment:
            has_frst = True
            # TODO Update Sepa_Informations.xlsx.
            logger.info(f"Erstlastschrift {order.verwendungszweck}")
            sepa_frst.add_payment(payment)
        else:
            has_rcur = True
            sepa_rcur.add_payment(payment)
    sepa_rcur_output = sepa_rcur.export().decode("utf-8") if has_rcur else None
    sepa_frst_output = sepa_frst.export().decode("utf-8") if has_frst else None
    return sepa_rcur_output, sepa_frst_output
