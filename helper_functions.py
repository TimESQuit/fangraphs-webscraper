import pandas as pd


def ip_fraction_handler(ip_series):
    """
    This function expects a series/list of numbers in the format of XX.Y
    where Y is one of 0, 1, or 2 and these numbers represent thirds of an inning.
    After converting the number format, it returns the sum of all numbers in the list
    as a real number rounded to 2 decimal places.
    """
    ip_wholes = 0
    ip_thirds = 0
    for ip_year in ip_series:
        if "." in str(ip_year):
            ip_wholes += int(str(ip_year).split(".")[0])
            ip_thirds += int(str(ip_year).split(".")[1])
    additional_wholes = ip_thirds // 3
    ip_wholes += additional_wholes
    ip_thirds = ip_thirds % 3
    return round((ip_wholes + ip_thirds / 3), 2)


def percentage_to_decimal(num_string):
    """
    This function assumes an input of either pd.isnull or a string in the format
    '[0-9][0-9].[0-9]%'. The function returns a real number in the format .[0-9][0-9][0-9]
    or pd.isnull, as appropriate.
    """
    if pd.isnull(num_string):
        return num_string
    else:
        num = num_string[:-1]
        return float(num) / 100
