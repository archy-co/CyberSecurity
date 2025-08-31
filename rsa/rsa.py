import random
from sympy import isprime, mod_inverse, nextprime
import hashlib

def generate_large_prime(bits=512):
    """Генерує велике просте число."""
    prime = random.getrandbits(bits)
    return nextprime(prime)

def generate_rsa_keys(bits=512):
    """
    Публічний ключ (Public Key): використовується для шифрування повідомлення або перевірки цифрового підпису. Він складається з:
    n: добуток двох великих простих чисел p і q.
    e: відкритий експонент, зазвичай це невелике просте число, наприклад, 65537.
    
    Приватний ключ (Private Key): використовується для розшифрування повідомлення або створення цифрового підпису. Він складається з:
    n: той самий, що і в публічному ключі.
    d: закрита експонента, яка є оберненою до e за модулем функції Ейлера ϕ(n)=(p−1)(q−1).
    """
    p = generate_large_prime(bits)
    q = generate_large_prime(bits)
    n = p * q
    phi = (p - 1) * (q - 1)

    e = 65537  # типове значення для e
    d = mod_inverse(e, phi)

    return (n, e), (n, d)  # Публічний і приватний ключі

def rsa_encrypt(message, public_key):
    """
    C = M^e mod(n)
    """
    n, e = public_key
    return [pow(ord(char), e, n) for char in message]

def rsa_decrypt(ciphertext, private_key):
    """
    M = C^d mod(n)
    """
    n, d = private_key
    return ''.join(chr(pow(char, d, n)) for char in ciphertext)

def generate_elgamal_keys(bits=512):
    """
    1. Публічний ключ (Public Key), для перевірки підпису:
    p: велике просте число.
    g: первісний корінь за модулем p.
    h: обчислюється як h = g^x mod(p), де x — закритий ключ.
    
    2. Приватний ключ (Private Key), для створення підпису:
    x: випадкове ціле число 1 < x < p−1.
    """
    p = generate_large_prime(bits)
    g = random.randint(2, p - 1)
    x = random.randint(1, p - 2)
    h = pow(g, x, p)
    return (p, g, h), x

def elgamal_sign(message, private_key, public_params):
    p, g, _ = public_params
    x = private_key

    # Обчислюємо хеш повідомлення
    hash_value = int(hashlib.sha256(message.encode()).hexdigest(), 16)

    # Знаходимо взаємно просте число k
    while True:
        k = random.randint(1, p - 2)
        if isprime(k) and mod_inverse(k, p - 1):
            break

    # Обчислюємо параметри підпису Ель Гамаля
    r = pow(g, k, p)
    k_inv = mod_inverse(k, p - 1)
    s = (k_inv * (hash_value - x * r)) % (p - 1)

    # Підпис - це пара r і s
    return r, s

def elgamal_verify(message, signature, public_params):
    p, g, h = public_params
    r, s = signature

    hash_value = int(hashlib.sha256(message.encode()).hexdigest(), 16)

    if r <= 0 or r >= p:
        return False

    # Перевірочні значення v1 та v2
    v1 = pow(g, hash_value, p)
    v2 = (pow(h, r, p) * pow(r, s, p)) % p
    return v1 == v2


if __name__ == "__main__":
    rsa_public_key, rsa_private_key = generate_rsa_keys()

    with open("message.txt", "r") as file:
        message = file.read()

    ciphertext = rsa_encrypt(message, rsa_public_key)
    with open("encrypted_message.txt", "w") as file:
        file.write(' '.join(map(str, ciphertext)))

    with open("encrypted_message.txt", "r") as file:
        ciphertext = list(map(int, file.read().split()))
    decrypted_message = rsa_decrypt(ciphertext, rsa_private_key)

    elgamal_public_params, elgamal_private_key = generate_elgamal_keys()

    signature = elgamal_sign(message, elgamal_private_key, elgamal_public_params)
    with open("signature.txt", "w") as file:
        file.write(f"{signature[0]} {signature[1]}")

    with open("signature.txt", "r") as file:
        r, s = map(int, file.read().split())

    is_valid = elgamal_verify(message, (r, s), elgamal_public_params)

    print(f"Відкрите повідомлення: {message}")
    print(f"Зашифроване повідомлення: {ciphertext}")
    print(f"Розшифроване повідомлення: {decrypted_message}")
    print(f"Цифровий підпис:\n r={r}\n s={s}")
    print(f"Підпис дійсний: {is_valid}")
