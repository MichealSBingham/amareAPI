#Testing and debugging 

from astrology.Constants import micheal 
from astrology.Constants import hirsch
from astrology.Constants import sahil
from astrology.Constants import kelle
import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def test():
    from prompts.astrology_traits_generator import PlacementInterpretationsGenerator
    print("testing....\n\n\n") 
    #install('openai')
    reader = PlacementInterpretationsGenerator()
    interpretation = reader.interpret_placement('male', 'North Node', 'Leo', '7th') 
    print(interpretation)
    

    



test() 
