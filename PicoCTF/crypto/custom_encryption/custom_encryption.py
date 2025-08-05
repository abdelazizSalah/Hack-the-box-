from random import randint
import sys


# g^x mod p
def generator(g, x, p):
    return pow(g, x) % p



def encrypt(plaintext, key):
    '''
        This function is responsible to encrypt the plaintext
        c = alphabetic order of char * key * 311
        order is the Ascii value of the character -> ord('a') = 97, ord('A') = 65
    '''
    cipher = []
    for char in plaintext:
        cipher.append(((ord(char) * key*311)))
    return cipher


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


def dynamic_xor_encrypt(plaintext, text_key):
    cipher_text = ""
    key_length = len(text_key)
    # iterate through each character in the plaintext in reverse order
    # and XOR it with the corresponding character in the key
    # if the key is shorter than the plaintext, it will repeat
    # the key until it matches the length of the plaintext
    for i, char in enumerate(plaintext[::-1]):
        key_char = text_key[i % key_length]
        encrypted_char = chr(ord(char) ^ ord(key_char))
        cipher_text += encrypted_char
    return cipher_text


def test(plain_text, text_key):
    p = 97
    g = 31
    if not is_prime(p) and not is_prime(g):
        print("Enter prime numbers")
        return
    a = randint(p-10, p)
    b = randint(g-10, g)
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
        return
    semi_cipher = dynamic_xor_encrypt(plain_text, text_key)
    cipher = encrypt(semi_cipher, shared_key)
    print(f'cipher is: {cipher}')


if __name__ == "__main__":
    message = sys.argv[1]
    test(message, "trudeau")
