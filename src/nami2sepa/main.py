#!/bin/env python

from concurrent.futures import ThreadPoolExecutor

import getpass
from nami2sepa import (
    logic,
    utils,
    input_output as io,
)

from pynami.nami import NaMi
import logging
import os
import warnings
warnings.filterwarnings('ignore')
logging.basicConfig(level=logging.INFO)


def _run_project(project_data, sepa_info, nami):
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for _, participant in project_data.iterrows():
            args=( 
                participant.Vorname, 
                participant.Nachname, 
                participant.Betrag,
                project_data,
                nami,
                sepa_info,
            )
            future = executor.submit(logic.gather_information, *args)
            futures.append(future)
        infos = [future.result() for future in futures]
    return infos


def _run_membership_payment(project_data, sepa_info, nami):
    active_members = nami.search(mglTypeId="MITGLIED", mglStatusId="AKTIV")
    infos = [
        logic.gather_information(
            member.vorname,
            member.nachname,
            project_data=project_data,
            nami=nami,
            sepa_info=sepa_info,
        )
        for member in active_members
    ]
    return infos


def run(project_path, output_path):
    sepa_info = io.open_sepa_info()
    if project_path is None:
        project_data = utils.find_input_file(".")
    else:
        project_data = io.open_project_file(project_path)

    infos = None
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    with NaMi(username=username, password=password) as nami:
        if len(project_data) > 0:
            infos = _run_project(project_data, sepa_info, nami)
        else:
            infos = _run_membership_payment(project_data, sepa_info, nami)
    io.output_xml(infos, output_path)


def new(project_name):
    curr_dir = os.getcwd()
    os.mkdir(os.path.join(curr_dir, project_name))


if __name__ == "__main__":
    run(None, "output.xml")
