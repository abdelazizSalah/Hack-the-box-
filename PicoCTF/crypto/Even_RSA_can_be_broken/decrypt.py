possible_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509]

# RSA public exponent (same as in encrypt.py)
e = 65537

N = 21615944640814547577507641006580386743696569448438899207202034403123310909248238758309097578318563250811647190576046113426440788972392459998825687001653878
ciphertext = 3531689653311876791070118231112421775350494072039337682177189742487672623755931063411998957923478398999526816470695036009721358599553334772417249332231929

for i in possible_primes:
    if N % i == 0:
        p = i
        q = N // p
        print(f"Found factors: p = {p}, q = {q}")
        break


# implementing extended eucliedean algorithm

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
        raise ValueError("Modular inverse does not exist")
    
    # Make sure the result is positive
    return (x_coeff % y + y) % y

def gen_key(p,q):
    """
    Generates RSA key with k bits
    """
    N = p*q
    d = inverse(e, (p-1)*(q-1))

    return ((N,e), d)


def decrypt(d,N, ciphertext):
    decrypted_int =  pow(ciphertext, d, N)
    # Convert integer back to bytes, then decode to string
    byte_length = (decrypted_int.bit_length() + 7) // 8
    decrypted_bytes = decrypted_int.to_bytes(byte_length, 'big')
    return decrypted_bytes.decode('utf-8') # Convert integer back to bytes, then decode to string
    

pubkey, d = gen_key(p, q)
decrypted = decrypt(d, N, ciphertext)

print('decrypted:', decrypted)


def encrypt(pubkey, m):
    N,e = pubkey
    return pow(m, e, N)
