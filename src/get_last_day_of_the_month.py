from time import gmtime, strftime
import datetime

def get_last_day_of_the_month():

    # Returns an integer representing the last day of the month
    # Algorithm: Take the first day of the next month, then count back
    # ward one day, that will be the last day of a given month. The
    # advantage of this algorithm is we don't have to determine the
    # leap year.

    y = int(strftime("%Y"))
    m = int(strftime("%m"))

    m += 1
    if m == 13:
        m = 1
        y += 1

    first_of_next_month = datetime.date(y, m, 1)
    last_of_this_month = first_of_next_month + datetime.timedelta(-1)
    return last_of_this_month.day
