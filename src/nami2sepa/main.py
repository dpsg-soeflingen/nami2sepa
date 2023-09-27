#!/bin/env python

import getpass
import os
import warnings
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
from loguru import logger
from pynami.nami import NaMi

from nami2sepa import input_output as io
from nami2sepa import logic, utils

warnings.filterwarnings("ignore")


def _run_project(project_data, sepa_info, nami):
    logger.info("Aktionsdaten werden gesammelt ...")
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for _, participant in project_data.iterrows():
            args = (
                participant.Vorname,
                participant.Nachname,
                participant.Betrag,
                participant.Verwendungszweck,
                project_data,
                nami,
                sepa_info,
            )
            future = executor.submit(logic.gather_information, *args)
            futures.append(future)
        infos = [future.result() for future in futures]
    return infos


def _run_membership_payment(project_data, sepa_info, nami):
    logger.info("Beitragszahlungsinformationen werden gesammelt ...")
    active_members = nami.search(mglTypeId="MITGLIED", mglStatusId="AKTIV")
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for member in active_members:
            args = (
                member.vorname,
                member.nachname,
                None,
                project_data.iloc[0].Verwendungszweck,
                project_data,
                nami,
                sepa_info,
            )
            future = executor.submit(logic.gather_information, *args)
            futures.append(future)
        infos = [future.result() for future in futures]
    return infos


def run(project_path, output_path):
    sepa_info = io.open_sepa_info()
    if project_path is None:
        project_data = utils.find_input_file(".")
    else:
        project_data = io.open_project_file(project_path)

    username = input("Benutzername: ")
    password = getpass.getpass("Passwort: ")
    with NaMi(username=username, password=password) as nami:
        if len(project_data) == 1 and pd.isnull(project_data.iloc[0].Vorname):
            infos = _run_membership_payment(project_data, sepa_info, nami)
        else:
            infos = _run_project(project_data, sepa_info, nami)
    logger.info(f"{len(infos)} Eintraege gefunden.")
    io.output_xml(infos, output_path)


def new(project_name):
    curr_dir = os.getcwd()
    os.mkdir(os.path.join(curr_dir, project_name))
