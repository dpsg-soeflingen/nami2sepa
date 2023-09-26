import logging

import pandas as pd

from nami2sepa import utils, xml_convert


def open_project_file(project_path):
    data = pd.read_excel(project_path)
    return data


def open_sepa_info():
    data = pd.read_excel("~/.config/nami2sepa/Sepa_Informations.xlsx", index_col="Mitgliedsnummer")
    return data


def write_file(content, file_path):
    with open(file_path, "w") as out_file:
        out_file.write(content)


def output_xml(data, path):
    rcur_output, frst_output = xml_convert.generate_xml(data)
    if rcur_output and frst_output:
        rcur_file_path = utils.modify_filename(path, "_rcur")
        frst_file_path = utils.modify_filename(path, "_frst")
        write_file(rcur_output, rcur_file_path)
        write_file(frst_output, frst_file_path)
        logging.info(f"Gespeichert in '{rcur_file_path}' und '{frst_file_path}'.")
    else:
        write_file(rcur_output or frst_output, path)
        logging.info(f"Gespeichert in '{path}'.")

