

def aspectBySign(sign1, sign2): 

    compatiblePairs = [('Water', 'Water'), 
                        ('Water', 'Earth'), 
                        ('Earth', 'Earth'), 
                        ('Earth', 'Water'), 
                        ('Air', 'Air'), 
                        ('Air', 'Fire'), 
                        ('Fire', 'Fire'), 
                        ('Fire', 'Air')
                        ]

    if sign1 == sign2: 
        return 'CONJUNCTION'
    elif signElement(sign1) == signElement(sign2) and (sign1 is not sign2): 
        return 'TRINE'
    elif (signElement(sign1), signElement(sign2) == compatiblePairs) and sign1 not in oppositions(sign2): 
        return 'SEXTILE'
    elif sign1 in oppositions(sign2): 
        return 'OPPOSITION'
    elif sign1 in squares(sign2): 
        return 'SQUARE'
    elif sign1 in semisextiles(sign2): 
        return 'SEMISEXTILE'
    else: 
        return 'QUINCUNX'
        




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
    



def semisextiles(sign):
    if 'Cancer': 
        return ['Gemini', 'Leo']
    if 'Leo': 
        return ['Cancer', 'Virgo']
    if 'Virgo':
        return ['Leo', 'Libra']
    if 'Libra':
        return ['Virgo', 'Scorpio']
    if 'Scorpio':
        return ['Libra', 'Sagittarius']
    if 'Sagittarius':
        return ['Scorpio', 'Capricorn']
    if 'Capricorn':
        return ['Sagittarius', 'Aquarius']
    if 'Aquarius':
        return ['Capricorn', 'Pisces']
    if 'Pisces':
        return ['Aquarius', 'Aries']
    if 'Aries':
        return ['Pisces', 'Taurus']
    if 'Taurus':
        return ['Aries', 'Gemini']
    if 'Gemini':
        return ['Taurus', 'Cancer']
    

def squares(sign): 
    if 'Aries' or 'Libra': 
        return ['Cancer', 'Capricorn']
    if 'Leo' or 'Aquarius': 
        return ['Taurus', 'Scorpio']
    if 'Sagittarius' or 'Gemini': 
        return ['Pisces', 'Virgo']

    if 'Taurus' or 'Scorpio': 
        return ['Leo', 'Aquarius']
    if 'Virgo' or 'Pisces': 
        return ['Sagittarius, Gemini']
    if 'Capricorn' or 'Cancer': 
        return ['Aries', 'Libra']


def oppositions(sign): 
    if 'Libra': 
        return 'Aries'
    if 'Aquarius': 
        return 'Leo'
    if 'Gemini': 
        return 'Sagittarius'
        
    if 'Cancer': 
        return 'Capricorn'
    if 'Pisces': 
        return 'Virgo'
    if 'Scorpio': 
        return 'Taurus'

    if 'Aries': 
        return 'Libra'
    if 'Leo': 
        return 'Aquarius'
    if 'Sagittarius': 
        return 'Gemini'

    if 'Taurus': 
        return 'Scorpio'
    if 'Capricorn': 
        return 'Cancer'
    if 'Virgo': 
        return 'Pisces'
    

    