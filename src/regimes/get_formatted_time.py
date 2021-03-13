def get_formatted_time(self, time_, format_, suffixes=None):
        """
        Convert float time to the given format (see timeFormats).
        :param time_:
        :param format_:
        :param suffixes:
        :return:
        """
        if math.isnan(time_):
            # Invalid time
            return '-----'
        if format_ == 'Float':
            return time_
        if suffixes is None:
            suffixes = ['AM', 'PM']

        time_ = self.fixhour(time_ + 0.5 / 60)  # add 0.5 minutes to round
        hours = math.floor(time_)

        minutes = math.floor((time_ - hours) * 60)
        suffix = suffixes[0 if hours < 12 else 1] if format_ == '12h' else ''
        formatted_time = "%02d:%02d" % (hours, minutes) if format_ == "24h" else "%d:%02d" % (
            (hours + 11) % 12 + 1, minutes)
        return "{time} {suffix}".format(time=formatted_time, suffix=suffix)
