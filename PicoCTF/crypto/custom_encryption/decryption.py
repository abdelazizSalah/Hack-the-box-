
from random import randint
import sys


# g^x mod p
def generator(g, x, p):
    return pow(g, x) % p



def decrypt(cipher_text, key):
    '''
        This function is responsible to encrypt the plaintext
        c = alphabetic order of char * key * 311
        order is the Ascii value of the character -> ord('a') = 97, ord('A') = 65
    '''
    semi_plaintext = []
    for char in cipher_text:
        semi_plaintext.append(chr(round(char / (key*311))))
    # print(f'semi_plaintext is: {semi_plaintext}')
    return "".join(semi_plaintext)



# this function check if the given number is prime or not.
def is_prime(p):
    v = 0
    for i in range(2, p + 1):
        if p % i == 0:
            v = v + 1
    if v > 1:
        return False
    else:
        return True


def reverse_dynamic_xor(cipher, text_key):
    plain_text = ""
    key_length = len(text_key)

    # notice that during the encryption, the string was reversed, so we need to process it as is, then reverse it at the end.
    for i, char in enumerate(cipher):
        key_char = text_key[i % key_length]
        encrypted_char = chr(ord(char) ^ ord(key_char))
        plain_text += encrypted_char
    return plain_text[::-1]

def Diffie_Hellman(a_plus,b_plus):
    p = 97
    g = 31
    if not is_prime(p) and not is_prime(g):
        print("Enter prime numbers")
        return -1
    # a = randint(p-10, p)
    # b = randint(g-10, g)
    a = a_plus
    b = b_plus
    print(f"a = {a}")
    print(f"b = {b}")
    u = generator(g, a, p)
    v = generator(g, b, p)
    key = generator(v, a, p)
    b_key = generator(u, b, p)
    shared_key = None
    if key == b_key:
        shared_key = key
    else:
        print("Invalid key")
        return -1
    return shared_key

def test(cipher_text, text_key):
    # for a in range (10):
    #     for b in range (10):
    shared_key = Diffie_Hellman(97,22)
    if shared_key == -1: return
    semi_plain_text = decrypt(cipher_text, shared_key)
    plain_text = reverse_dynamic_xor(semi_plain_text, text_key)

    print(f'plainText is: {plain_text}')


if __name__ == "__main__":
    message = [151146, 1158786, 1276344, 1360314, 1427490, 1377108, 1074816, 1074816, 386262, 705348, 0, 1393902, 352674, 83970, 1141992, 0, 369468, 1444284, 16794, 1041228, 403056, 453438, 100764, 100764, 285498, 100764, 436644, 856494, 537408, 822906, 436644, 117558, 201528, 285498]
    test(message, "trudeau")

