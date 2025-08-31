import numpy as np
import string
from numpy.linalg import inv
from sympy import Matrix
import math

# Example of key which will make invertible matrix: jajdhfkjbioyobqb

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def is_invertible_mod_26(matrix):
    det = int(np.round(np.linalg.det(matrix))) % 26
    if gcd(det, 26) != 1:
        return False, det
    return True, det

def text_to_numbers(text):
    alphabet = string.ascii_uppercase
    text = text.upper().replace(" ", "")
    numbers = [alphabet.index(char) for char in text if char in alphabet]
    return numbers

def numbers_to_text(numbers):
    alphabet = string.ascii_uppercase
    text = ''.join([alphabet[num % 26] for num in numbers])
    return text

def generate_key_matrix(keyword):
    keyword = keyword.upper().replace(" ", "")
    keyword_numbers = text_to_numbers(keyword)
    if len(keyword_numbers) < 9:
        raise ValueError("Key should be at least 9 letters long.")
    
    key_matrix = np.array(keyword_numbers[:9]).reshape(3, 3)
    
    invertible, det = is_invertible_mod_26(key_matrix)
    if not invertible:
        raise ValueError(f"Key matrix is not invertible with mod 26. Choose another keyword.")
    
    print("Key matrix:")
    print(key_matrix)
    return key_matrix

def hill_cipher_encrypt(plaintext, key_matrix):
    plaintext_numbers = text_to_numbers(plaintext)
    
    # Make length divisible by 3
    while len(plaintext_numbers) % 3 != 0:
        plaintext_numbers.append(0)
    
    plaintext_matrix = np.array(plaintext_numbers).reshape(-1, 3).T
    encrypted_matrix = np.dot(key_matrix, plaintext_matrix) % 26
    
    encrypted_numbers = encrypted_matrix.T.flatten()
    encrypted_text = numbers_to_text(encrypted_numbers)
    
    return encrypted_text

def hill_cipher_decrypt(ciphertext, key_matrix):
    ciphertext_numbers = text_to_numbers(ciphertext)
    
    # Inverted matrix with mod 26
    try:
        key_matrix_mod_inv = Matrix(key_matrix).inv_mod(26)
    except:
        raise ValueError("Key matrix is not invertible. Decryption not possible.")
    
    key_matrix_inv = np.array(key_matrix_mod_inv).astype(int)
    
    ciphertext_matrix = np.array(ciphertext_numbers).reshape(-1, 3).T
    decrypted_matrix = np.dot(key_matrix_inv, ciphertext_matrix) % 26
    
    decrypted_numbers = decrypted_matrix.T.flatten()
    decrypted_text = numbers_to_text(decrypted_numbers)
    
    return decrypted_text

def encrypt_file(input_file, keyword, output_file):
    with open(input_file, 'r') as file:
        plaintext = file.read()
    
    key_matrix = generate_key_matrix(keyword)
    encrypted_text = hill_cipher_encrypt(plaintext, key_matrix)
    
    with open(output_file, 'w') as file:
        file.write(encrypted_text)
    
    print(f"Encrypted message is written to file <{output_file}>")

def decrypt_file(input_file, keyword, output_file):
    with open(input_file, 'r') as file:
        ciphertext = file.read()
    
    key_matrix = generate_key_matrix(keyword)
    decrypted_text = hill_cipher_decrypt(ciphertext, key_matrix)
    
    with open(output_file, 'w') as file:
        file.write(decrypted_text)
    
    print(f"Decrypted message is written to file <{output_file}>")
    print("Decrypted message:")
    print(decrypted_text)

if __name__ == "__main__":
    keyword = input("Enter keyword: ")
    encrypt_file('plaintext.txt', keyword, 'encrypted.txt')
    decrypt_file('encrypted.txt', keyword, 'decrypted.txt')
