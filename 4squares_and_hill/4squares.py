import string

def prepare_key(key):
    """
    Remove duplicates from key
    """
    result = []
    for char in key:
        if char not in result and char in string.ascii_uppercase:
            result.append(char)
    return ''.join(result)

def generate_square(key):
    """
    5x5 square
    """
    key = prepare_key(key)
    square = key + ''.join([char for char in string.ascii_uppercase if char not in key and char != 'J'])
    return [list(square[i:i+5]) for i in range(0, 25, 5)]

def find_position(square, char):
    """
    coordinates of symbol in square
    """
    for row_idx, row in enumerate(square):
        if char in row:
            return row_idx, row.index(char)
    return None

def encrypt_bigram(square1, square2, bigram):
    pos1 = find_position(square1, bigram[0])
    pos2 = find_position(square2, bigram[1])
    return square1[pos1[0]][pos2[1]] + square2[pos2[0]][pos1[1]]

def decrypt_bigram(square1, square2, bigram):
    pos1 = find_position(square1, bigram[0])
    pos2 = find_position(square2, bigram[1])
    return square1[pos1[0]][pos2[1]] + square2[pos2[0]][pos1[1]]

def encrypt(text, key1, key2):
    square1 = generate_square(key1)
    square2 = generate_square(key2)
    
    text = text.upper().replace('J', 'I')   # cuz it's 5x5 square, but alphabet is 26 letters, so we treat J same as I
    if len(text) % 2 != 0:
        text += 'X'     # fake symbol in number of characters is odd

    encrypted_text = ''
    for i in range(0, len(text), 2):
        bigram = text[i:i+2]
        encrypted_bigram = encrypt_bigram(square1, square2, bigram)
        encrypted_text += encrypted_bigram
    return encrypted_text

def decrypt(text, key1, key2):
    square1 = generate_square(key1)
    square2 = generate_square(key2)
    
    decrypted_text = ''
    for i in range(0, len(text), 2):
        bigram = text[i:i+2]
        decrypted_bigram = decrypt_bigram(square1, square2, bigram)
        decrypted_text += decrypted_bigram
    return decrypted_text

def main():
    key1 = input("1st key (only letters): ").upper()    # for the first square
    key2 = input("2nd key (only letters): ").upper()    # for the second square

    text = input("Secret (only letters): ").upper()

    try:
        encrypted_text = encrypt(text, key1, key2)
        print(f"Encrypted: {encrypted_text}")

        decrypted_text = decrypt(encrypted_text, key1, key2)
        print(f"Decrypted: {decrypted_text}")
    except TypeError as err:
        print("Error occurred! Only English letters are accepted (no spaces, number, other characters etc.)")

if __name__ == "__main__":
    main()
