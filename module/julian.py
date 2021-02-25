@staticmethod
def julian(year, month, day):
        """
        Convert Gregorian date to Julian day.
        Ref: Astronomical Algorithms by Jean Meeus.
        :param year:
        :param month:
        :param day:
        :return:
        """
        if month <= 2:
            year -= 1
            month += 12
        a = math.floor(year / 100)
        b = 2 - a + math.floor(a / 4)
        return math.floor(365.25 * (year + 4716)) + math.floor(30.6001 * (month + 1)) + day + b - 1524.5
