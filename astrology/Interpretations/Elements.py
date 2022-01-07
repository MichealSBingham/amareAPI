class Element:

    def info(self):
        return "The basic temperament of the sign. The nature of the sign."


class Fire(Element):

    def signs(self):
        """
        :return: A list of signs belonging to this element (fire)
        """
        #TODO: Make signs an object and return the objects instead of strings
        return ['Aries', 'Leo', 'Sagittarius']

    # TODO: Make descriptions for the signs (Aries must act, Leo must lead, Sagittarius must explore)
    def description(self):
        """
        :return: The general description of this element. 'Fire' is used the pronoun for the persom.
        """
        return 'Fire will respond to energy quickly. Fire will take a risk and is ready to take action. Fire is the first to go.'

    #TODO (https://astrolibrary.org/fire-sign-love-language/)
    def love_language(self):
        pass

    #TODO
    def love_language_receiving(self):
        pass

    def keywords(self, polarity: bool = None) -> [str]:
        """

        :param polarity: If True, will return justpositive traits, if False will return negative trains. Otherwise, all traits will be returned
        :return: A list of traits
        :rtype: str
        """
        if polarity == True:
            return [""]
        elif polarity == False:
            return [""]
        else:
            return [""]



