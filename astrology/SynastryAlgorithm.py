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
    