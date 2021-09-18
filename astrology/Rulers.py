class Rulers:

    def ruler_of( sign):
        """
        Returns the ruler of the sign. Example if the sign is 'Cancer', its ruler will be 'Moon'
        :return: The planet that the sign rules
        :rtype: str
        :param sign: The zodiac sign string, e.g. 'Cancer', 'Scorpio', etc.
        :type sign: str
        """

        if sign == 'Cancer':
            return 'Moon'
        elif sign == 'Aries':
            return 'Mars'
        elif sign == 'Taurus':
            return 'Venus'
        elif sign == 'Gemini':
            return 'Mercury'
        elif sign == 'Leo':
            return 'Sun'
        elif sign == 'Virgo':
            return 'Mercury'
        elif sign == 'Scorpio':
            return 'Mars'
        elif sign == 'Sagittarius':
            return 'Jupiter'
        elif sign == 'Pisces':
            return 'Jupiter'
        elif sign == 'Libra':
            return 'Venus'
        elif sign == 'Capricorn':
            return 'Saturn'
        elif sign == 'Aquarius':
            return 'Saturn'
        else:
            return ""




    def modernRulerOf(self, sign):
        pass