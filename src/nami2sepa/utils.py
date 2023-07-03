import datetime
import os
import pandas as pd


def join(df1, df2):
    """
    Combine sepa and sepa_dates
    """
    return df1.join(df2.set_index("Mandat"), on="Mandat")


def is_today(date: datetime.datetime):
    return date.date() == datetime.date.today()


def infer_file_names(scan_dir, **file_types):
    for file_name in os.listdir(scan_dir):
        file_name = scan_dir + "/" + file_name
        if file_name.endswith("xlsx"):
            if file_types["accounts"] is None or file_types["tasks"] is None:
                columns = pd.read_excel(file_name).columns
                if "Taetigkeit_in_Gruppierung" in columns \
                    and file_types["tasks"] is None:
                    file_types["tasks"] = file_name
                elif "Kontonummer" in columns \
                    and file_types["accounts"] is None:
                    file_types["accounts"] = file_name
        elif file_name.endswith("json"):
            if file_types["project"] is None:
                file_types["project"] = file_name
    return file_types



