# Ревера Ярослав. ПМІ45
# Варіант 9 (x^11+x^2+1)

def lfsr_feedback(state, taps):
    """Обчислює зворотний зв'язок для LFSR."""
    feedback = 0
    for tap in taps:
        feedback ^= (state >> (tap - 1)) & 1
    return feedback

def generate_lfsr_key(n, taps, seed, length):
    """
    Генерує ключ для шифрування за допомогою LFSR.
    
    n - розрядність регістра
    taps - позиції зворотного зв'язку (відповідають поліному)
    seed - початковий стан
    length - довжина ключа
    """
    state = seed
    key = []
    print(f"{'Номер Стану':<15}{'Внутрішній Стан':<25}{'Зворотній Звʼязок':<20}{'Біт на Виході':<15}")
    print("-" * 75)
    for step in range(length):
        output_bit = state & 1
        feedback = lfsr_feedback(state, taps)
        print(f"{step + 1:<15}{bin(state)[2:].zfill(n):<25}{feedback:<20}{output_bit:<15}")
        key.append(output_bit)
        state = (state >> 1) | (feedback << (n - 1))
    return key

def xor_encrypt_decrypt(data, key):
    """Шифрує або дешифрує дані шляхом XOR з ключем."""
    return [bit ^ key[i % len(key)] for i, bit in enumerate(data)]

if __name__ == "__main__":
    n = 11                  # розрядність регістра
    taps = [11, 2]          # позиції зворотного зв'язку для x^11 + x^2 + 1
    seed = 0b10110100101    # початковий стан (наприклад, 11-бітове число)
    length = 32

    key = generate_lfsr_key(n, taps, seed, length)

    plaintext = [1, 0, 1, 1, 0, 0, 1, 1]
    print("\nТекст:", plaintext)
    ciphertext = xor_encrypt_decrypt(plaintext, key)
    print("Зашифрований текст:", ciphertext)

    decrypted_text = xor_encrypt_decrypt(ciphertext, key)
    print("Розшифрований текст:", decrypted_text)
