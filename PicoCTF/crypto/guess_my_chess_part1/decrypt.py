# Trying affine cipher bruteforce
import string

cipher = 'TORSSVE'

alphabet_map = {c:i for i,c in enumerate(string.ascii_uppercase)}
index_map = {i:c for i,c in enumerate(string.ascii_uppercase)}


def inverse(x, y):
    """
    Computes the modular inverse of x modulo y using extended Euclidean algorithm
    Returns x^(-1) mod y
    """
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        
        return gcd, x, y
    
    gcd, x_coeff, y_coeff = extended_gcd(x % y, y)
    
    if gcd != 1:
        return -1
    
    # Make sure the result is positive
    return (x_coeff % y + y) % y

import string
cipher = 'RANWAQZKFSVQA'

alphabet_map = {c:i for i,c in enumerate(string.ascii_uppercase)}
index_map = {i:c for i,c in enumerate(string.ascii_uppercase)}

a_1 = 9
b = 9

plain = ''
for c in cipher:
    c_num = alphabet_map[c]
    m = index_map[(c_num * a_1) % 26]
    plain += m
print(plain)

print(inverse(3,26))