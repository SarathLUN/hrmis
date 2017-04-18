__author__ = 'Tusfiqur'

from datetime import date, datetime

def convert_to_date(date_string):

    new_date = None
    if len(date_string) <= 7:
        new_date = None

    elif date_string[4]== '/' and date_string[7] == '/':

        new_date = datetime.strptime(date_string, "%Y/%m/%d")

    elif date_string[6] == ',':

        new_date = datetime.strptime(date_string, "%b %d, %Y")

    return new_date