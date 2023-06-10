import datetime


def join(df1, df2):
    """
    Combine sepa and sepa_dates
    """
    return df1.join(df2.set_index("Mandat"), on="Mandat")


def is_today(date: datetime.datetime):
    return date.date() == datetime.date.today()

