import binascii, os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def create_hex_table(file_path):
    hex_table = []

    with open(file_path, 'r',errors='replace') as file:
        bytes_data = file.read()

    num_bytes = len(bytes_data)
    print(f"Generating possible keys from file: {file_path}")

    for i in range(num_bytes - 31):
        hex_sequence = bytes_data[i:i+32]
        try:
            test = binascii.unhexlify(hex_sequence).hex()
            hex_table.append(hex_sequence)
        except:
            pass
        if i % 100000 == 0:
            progress = (i / num_bytes) * 100
            print(f"{progress:.2f}%", end='\r')
    print("Deleting duplicate keys")
    hex_table=list(set(hex_table))
    return hex_table

def decrypt_file(input_file, output_file, key_hex):
    try:
        block_size = algorithms.AES.block_size // 8
        key = binascii.unhexlify(key_hex)

        with open(input_file, 'rb') as file:
            ciphertext = file.read()

        iv = ciphertext[:block_size]
        ciphertext = ciphertext[block_size:]

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()

        padding_length = plaintext[-1]
        plaintext = plaintext[:-padding_length]

        try:
            if len(plaintext) > 0:
                #plaintext2 = plaintext.decode("utf-8")
                with open(output_file, 'wb') as file:
                    file.write(plaintext)
                return True
            else:
               return False
        except Exception:
            return False
    except Exception:
        return False

def encrypt_file(input_file, output_file, key_hex, useHeader=False):
    try:
        block_size = algorithms.AES.block_size // 8
        key = binascii.unhexlify(key_hex)

        with open(input_file, 'rb') as file:
            plaintext = file.read()

        fname, file_extension = os.path.splitext(input_file)

        if useHeader:
            header = fname + ".cud"
            if not os.path.isfile(header):
                print("Header file missing")
                return False

            with open(header, 'rb') as file:
                headertext = file.read()

            iv = headertext[:block_size]
        else:
            iv = os.urandom(16)

        plaintext = plaintext + (b'\x0B' * (block_size - len(plaintext) % block_size))

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = iv + encryptor.update(plaintext) + encryptor.finalize()

        with open(output_file, 'wb') as file:
            file.write(ciphertext)
    except Exception as e:
        print(e)
        return False

def main():
    input_file = 'test.cud'
    key_path = "libSGF.so"
    result = create_hex_table(key_path)
    keys = result
    print("Testing generated keys:")
    print()
    for i, key_hex in enumerate(keys, 1):
        output_file = f"{key_hex}.json"
        success = decrypt_file(input_file, output_file, key_hex)
        if i % 1000 == 0:
            progress2 = (i / len(keys)) * 100
            print(f"{progress2:.3f}%", end='\r')
        if success:
            print(f"Good key found: {key_hex}")
            break

    if not success:
        print("Key not found")

if __name__ == "__main__":
    main()
    input()