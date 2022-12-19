# Moises Shalimay Andrade
# Auxiliary module with functions that tests if strings are numbers and convert them

import re 

#=======================================
#SECTION check if strings are numbers
#=======================================

def str_is_integer(astring:str, consider_floats = True, consider_fractions = True):
    """ Returns a boolean indicating if a string is an integer. 
    
    Args:
        asstring (str): a string potentially containing an integer
        consider_floats (bool): boolean indicating if should consider 'x.0' an integer
        consdider_fractions (bool): boolean indicating if should consider 'x/x' an integer

    Returns:
        boolean: True if the string is an integer; false otherwise

    Examples:
        str_is_integer('3') -> True

        str_is_integer('3/3', consider_fractions=True) -> True ; str_is_integer('3/3', consider_fractions=False) -> False
        str_is_integer('2/3', consider_fractions=True|False) -> False

        str_is_integer('3.0', consider_floats=True) -> True; str_is_integer('3.0', consider_floats=False) -> False; 
        str_is_integer('2.5', consider_floats=True|False) -> False
    """

    if not all(consider_floats, consider_fractions):
        try: 
            int(astring)
            return True
        except:
            return False
            

    else:
        if not is_number(astring):
            return False

        # if is a number, but is a fraction, test if it is in the format ('a/a')
        elif is_fraction(astring):
            numerator_denominator = astring.split('/')
            if numerator_denominator[0] == numerator_denominator[1]:
                return True
            else:
                return False

        # it is a number and not a fraction:
                # float in the format  a.x, x>0 -> not integer
                # float in the format 'x.0'  ----> integer
        else:
            if num_is_integer(float(astring)):
                return True
            else:
                return False



def is_numberdigit(astring:str, remove_whitespaces = True):
    """check if a string is a number in the format "x or abc.def" and return True or False; dont consider fractions

    Obs1.: The function ignores whitespaces in strings, but spaces happen BETWEEN characters, the function will return False. Eg.: '3 .5' = False.
    Obs2.: This function is an auxiliary to construct the "is_fraction" function without getting into circularity ("is_fraction" test if digits are floats), 
    both are then consolidated in the full 'is_number' function
    """
    # remove whitespaces and potential spaces between numbers for further evaluation
    if remove_whitespaces:
        astring = astring.replace(r'\s',"")
        
    try:
        float(astring)
        return True
    except:
        return False

def is_fraction(astring:str, remove_whitespaces = True):
    """ Checks if a string is a fraction in the format "a/b" and returns True or False
    Obs.: float/integer is also considered as a fraction (e.g., 3.5/4 or pi/3 are fractions)""" 
    # if does not find the "/", not a fraction
    if astring.find("/")==-1:
        return False
    else:
        # remove whitespaces and potential spaces between numbers for further evaluation
        if remove_whitespaces:
            astring = re.sub(r'\s', astring)

        # if there are two chrs separated by "/" and all them are numbers -> Fraction
        numerator_denominator = astring.split('/')
        if len(numerator_denominator) == 2 and all(is_numberdigit(charach) for charach in numerator_denominator):
            return True
        else:
            return False

def is_number(astring:str):
    """check if a string is a number and return True or False. Consider fractions

    Obs1.: The function ignores whitespaces in strings, but spaces happen BETWEEN characters, the function will return False. 
    Obs2.: Consider fractions in the format 'a/b'
    """
    # check if string is a fraction (a/b)
    if is_fraction(astring):
        return True
    
    # check if string is a number in the format "x" or "abc.def"
    elif is_numberdigit(astring):
        return True

    else:
        return False


#/SECTION
#=======================================================================
#SECTION Convert string to floats/integers
#=======================================================================
def fraction_to_float(astring:str):
    """ Converts a string that is a fraction to a float"""
    numerator_denominator = astring.split('/')
    return float(numerator_denominator[0])/float(numerator_denominator[1])


def str_to_number(astring: str):
    """Converts a string to a number
    Returns: a float or None
    """
    number = None
    # if it is a number, convert to float (deal with fractions separately)
    if is_fraction(astring):
        number = fraction_to_float(astring)
    else:
        number = float(astring)
    return number



#/SECTION
#=======================================================================
#SECTION Check integers/floats properties
#=======================================================================

def num_is_integer(number):
    if isinstance(number,int):
        return True

    if isinstance(number,float):
        return number.is_integer()

    return False
