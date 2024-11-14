from datetime import datetime
import re

def validate_date_in_YYYYMMDDHHmmFormat(dateToValidate):
    if not re.match(r"[0-9]{4}-[0-9]{2}-[0-9]{2}\s(0?[0-9]|1[0-9]|2[0-3]):[0-9]+", dateToValidate):
        raise ValueError("Invalid date format. Date format must be YYYY-MM-DD hh:mm")

    try:
        datetime.strptime(dateToValidate, '%Y-%m-%d %H:%M')
    except ValueError:
        raise ValueError("The given " + dateToValidate + " is not a valid date")

    return dateToValidate