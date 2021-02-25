def sun_position(self, jd):
        """
        Compute declination angle of sun and equation of time.
        Ref: http://aa.usno.navy.mil/faq/docs/SunApprox.php
        :param jd:
        :return:
        """
        d = jd - 2451545.0
        g = self.fixangle(357.529 + 0.98560028 * d)
        q = self.fixangle(280.459 + 0.98564736 * d)
        l = self.fixangle(q + 1.915 * self.sin(g) + 0.020 * self.sin(2 * g))

        # R = 1.00014 - 0.01671 * self.cos(g) - 0.00014 * self.cos(2 * g)
        e = 23.439 - 0.00000036 * d

        ra = self.arctan2(self.cos(e) * self.sin(l), self.cos(l)) / 15.0
        eqt = q / 15.0 - self.fixhour(ra)
        decl = self.arcsin(self.sin(e) * self.sin(l))

        return decl, eqt
