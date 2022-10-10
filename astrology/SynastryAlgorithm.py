# This is a helper class to determine element, modality, and sign of a planet and or house 







def elementalHarmony(self):

    from astrology.NatalChart import getElement

        #if self.type == aspectFromDeg(const.OPPOSITION) and self.orb < 8.0:
            #return False
    (element1, element2) = (getElement(self.first, set_orb=0), getElement(self.second, set_orb=0))

    if element1 == element2:
        return True

    if (element1, element2) == ('Water', 'Fire') or (element1, element2) == ('Fire', 'Water'):
        return False

    if (element1, element2) == ('Water', 'Air') or (element1, element2) == ('Air', 'Water'):
        return False

    if (element1, element2) == ('Earth', 'Air') or (element1, element2) == ('Air', 'Earth'):
        return False
    
    if (element1, element2) == ('Earth', 'Fire') or (element1, element2) == ('Fire', 'Earth'):
        return False

    return True

def elementalHarmonyBetweenSigns(sign1, sign2):
    from astrology.NatalChart import getElement

        #if self.type == aspectFromDeg(const.OPPOSITION) and self.orb < 8.0:
            #return False
    (element1, element2) = (signElement(sign1), signElement(sign2))

    if element1 == element2:
        return True

    if (element1, element2) == ('Water', 'Fire') or (element1, element2) == ('Fire', 'Water'):
        return False

    if (element1, element2) == ('Water', 'Air') or (element1, element2) == ('Air', 'Water'):
        return False

    if (element1, element2) == ('Earth', 'Air') or (element1, element2) == ('Air', 'Earth'):
        return False
    
    if (element1, element2) == ('Earth', 'Fire') or (element1, element2) == ('Fire', 'Earth'):
        return False

    return True

def signElement(sign): 
    if sign == 'Cancer' or sign =='Pisces' or sign == 'Scorpio':
        return 'Water' 
    elif sign == 'Leo' or sign == 'Sagittarius' or sign == 'Aries': 
        return 'Fire'
    elif sign == 'Libra' or sign == 'Gemini' or sign =='Aquarius':
        return 'Air'
    elif sign == 'Capricorn' or sign == 'Virgo' or sign == 'Taurus': 
        return 'Earth'


def modality(sign): 
    if sign == 'Scorpio' or sign == 'Leo' or sign == 'Aquarius' or sign == 'Taurus': 
        return 'Fixed'
    elif sign == 'Pisces' or sign == 'Sagittarius' or sign == 'Gemini' or sign == 'Virgo': 
        return 'Mutable'
    else: 
        'Cardinal'
    

def houseElement(houseNumber):
    if houseNumber == 1 or houseNumber == 5 or houseNumber == 9: 
        return 'Fire'
    elif houseNumber == 2 or houseNumber == 6 or houseNumber == 10: 
        return 'Earth'
    elif houseNumber == 3 or houseNumber == 7 or houseNumber == 11: 
        return 'Air'
    elif houseNumber == 4 or houseNumber == 8 or houseNumber == 12: 
        return 'Water'
    else: 
        return 'Error'


def receptiveOrOutgoing(houseNumber):
    if (houseNumber % 2 == 0 ): 
        return 'Receptive'
    else:
        return 'Outgoing'



def semisextiles(sign):
    if sign == 'Cancer': 
        return ['Gemini', 'Leo']
    if sign == 'Leo': 
        return ['Cancer', 'Virgo']
    if sign == 'Virgo':
        return ['Leo', 'Libra']
    if sign == 'Libra':
        return ['Virgo', 'Scorpio']
    if sign == 'Scorpio':
        return ['Libra', 'Sagittarius']
    if sign == 'Sagittarius':
        return ['Scorpio', 'Capricorn']
    if sign == 'Capricorn':
        return ['Sagittarius', 'Aquarius']
    if sign == 'Aquarius':
        return ['Capricorn', 'Pisces']
    if sign == 'Pisces':
        return ['Aquarius', 'Aries']
    if sign == 'Aries':
        return ['Pisces', 'Taurus']
    if sign == 'Taurus':
        return ['Aries', 'Gemini']
    if sign == 'Gemini':
        return ['Taurus', 'Cancer']
    

def squares(sign): 
    if sign == 'Aries' or sign ==  'Libra': 
        return ['Cancer', 'Capricorn']
    if sign == 'Leo' or sign == 'Aquarius': 
        return ['Taurus', 'Scorpio']
    if sign == 'Sagittarius' or sign == 'Gemini': 
        return ['Pisces', 'Virgo']

    if sign == 'Taurus' or sign == 'Scorpio': 
        return ['Leo', 'Aquarius']
    if sign == 'Virgo' or sign == 'Pisces': 
        return ['Sagittarius, Gemini']
    if sign == 'Capricorn' or sign == 'Cancer': 
        return ['Aries', 'Libra']


def oppositions(sign): 
    if sign == 'Libra': 
        return 'Aries'
    if sign == 'Aquarius': 
        return 'Leo'
    if sign == 'Gemini': 
        return 'Sagittarius'
        
    if sign == 'Cancer': 
        return 'Capricorn'
    if sign == 'Pisces': 
        return 'Virgo'
    if sign == 'Scorpio': 
        return 'Taurus'

    if sign == 'Aries': 
        return 'Libra'
    if sign == 'Leo': 
        return 'Aquarius'
    if sign == 'Sagittarius': 
        return 'Gemini'

    if sign == 'Taurus': 
        return 'Scorpio'
    if sign == 'Capricorn': 
        return 'Cancer'
    if sign == 'Virgo': 
        return 'Pisces'
    



def aspectBySign(firstSign, secondSign): 
    degrees = {'Aries': 0, 'Taurus': 30, 'Gemini': 60, 'Cancer': 90, 'Leo': 120, 'Virgo': 150, 'Libra': 180, 'Scorpio': 210, 'Sagittarius': 240, 'Capricorn': 270, 'Aquarius': 300, 'Pisces': 330}
    deg = abs(degrees[firstSign] - degrees[secondSign])

    if abs(deg) > 180:
        deg = abs(360 - deg)
    
    if abs(deg) > 180: 
        deg = abs(360 - deg)

        
    if deg == 0:
        return 'CONJUNCTION'
    elif deg == 30:
        return 'SEMISEXTILE'
    elif deg == 60:
        return 'SEXTILE'
    elif deg == 90:
        return 'SQUARE'
    elif deg == 120:
        return 'TRINE'
    elif deg == 150:
        return 'QUINCUNX'
    elif deg == 180:
        return 'OPPOSITION'
    else:
        return 'NONE'
    