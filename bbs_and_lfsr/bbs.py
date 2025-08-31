import random
from sympy import nextprime

def generate_large_prime(bits=512):
    """Генерує велике просте число."""
    prime = random.getrandbits(bits)
    return nextprime(prime)

def generate_bbs_key():
    """Генерує параметри p, q, n для генератора BBS."""
    p = generate_large_prime()
    q = generate_large_prime()
    while q == p:
        q = generate_large_prime()
    n = p * q
    x = random.randint(2, n - 1)
    while x % p == 0 or x % q == 0:
        x = random.randint(2, n - 1)
    return p, q, n, x

def bbs_random_bit_generator(n, x, length):
    """Генерує послідовність випадкових бітів на основі генератора BBS."""
    random_bits = []
    for _ in range(length):
        x = pow(x, 2, n)    # x_i+1 = (x_i)^2 % n
        random_bits.append(x % 2)
    return random_bits

def encrypt_decrypt_bbs(message, key_stream):
    """Шифрує або дешифрує повідомлення за допомогою потокового ключа."""
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    # Для шифрування/дешифрування використовується XOR між повідомленням (у вигляді бінарного рядка) і ключовим потоком
    # (XOR симетричний, тому одні і тіж операції для шифрування і дешифрування)
    encrypted_binary = ''.join(str(int(bit) ^ key_stream[i]) for i, bit in enumerate(binary_message))
    encrypted_message = ''.join(chr(int(encrypted_binary[i:i+8], 2)) for i in range(0, len(encrypted_binary), 8))
    return encrypted_message

if __name__ == "__main__":
    message = "Hello, BBS Stream Cipher!"
    print(f"Повідомлення: {message}")

    p, q, n, x = generate_bbs_key()
    print(f"Прості числа:\n p = {p}\n q = {q}")
    # print(f"Модуль n = {n}\nПочаткове значення x = {x}")

    key_stream = bbs_random_bit_generator(n, x, len(message) * 8)
    # print(f"Ключовий потік: {''.join(map(str, key_stream))}")

    encrypted_message = encrypt_decrypt_bbs(message, key_stream)
    print(f"Зашифроване повідомлення: {encrypted_message}")

    decrypted_message = encrypt_decrypt_bbs(encrypted_message, key_stream)
    print(f"Розшифроване повідомлення: {decrypted_message}")
