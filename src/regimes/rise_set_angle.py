@staticmethod
def rise_set_angle(elevation=0):
        """
        Return sun angle for sunset/sunrise.
        :param elevation:
        :return:
        """
        elevation = 0 if elevation is None else elevation
        return 0.833 + 0.0347 * math.sqrt(elevation)  # an approximation
