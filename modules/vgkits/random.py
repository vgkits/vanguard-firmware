from os import urandom
from math import floor

def randint(minVal, maxVal=None):
    '''
    Calculates a 'uniformly' distributed random integer up to and excluding bound.
    Draws enough bytes from the random number generator for every possible bit up
    to the bound to be populated, plus an extra byte. Sequencing these bytes creates
    a random number at least 256 times larger than the target bound. This number modulus
    the range then produces an integer result within bounds. [Cefn Hoile]
    '''
    if(maxVal!=None):
        return minVal + randint(maxVal-minVal)
    else:
        maxVal=minVal
    byteCount = (log2approx(maxVal) // 8) + 1 # each byte is 8 powers of two
    val = 0
    for idx, entry in enumerate(bytearray(urandom(byteCount))):
        val |= entry << (idx * 8)
    return val % maxVal


def pick(entries):
    """Selects an entry from a list at random
    :param entries: list to select from
    :return: a single entry
    """
    return entries[randint(len(entries))]


def log2approx(val):
    '''
    Efficient calculation for the logarithm of val, (to the base 2), rounded
    up to the next whole number. It rounds down to nearest integer, then unsets
    individual bits of the int() until val is 0. The final bit unset is the largest
    power of 2 in val, allowing us to calculate an upper bound on the logarithm. [Cefn Hoile]
    '''
    val = floor(val)
    approx = 0
    while val != 0:
        val &= ~ (1<<approx)
        approx = approx + 1
    return approx
