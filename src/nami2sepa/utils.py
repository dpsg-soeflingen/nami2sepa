import os

import pandas as pd
from loguru import logger


def modify_filename(file_path, addition):
    directory = os.path.dirname(file_path)
    basename = os.path.basename(file_path)

    name, extension = os.path.splitext(basename)
    new_basename = name + addition + extension
    new_file_path = os.path.join(directory, new_basename)

    return new_file_path


def find_input_file(root_directory):
    for file_name in os.listdir(root_directory):
        file_name = root_directory + "/" + file_name
        if file_name.endswith("xlsx"):
            found_file = pd.read_excel(file_name)
            columns = found_file.columns
            if "Vorname" in columns:
                logger.info(f"Verwende Input-Datei {file_name}.")
                return found_file
    logger.error("Keine gueltigen Dateien im Quellverzeichnis gefunden.")
    exit(1)
