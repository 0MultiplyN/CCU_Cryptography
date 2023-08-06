import os
import base64
import time
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


def generate_key_and_iv(key_length):
    # Generate a random key
    key = os.urandom(key_length)
    # Generate a random IV
    iv = os.urandom(16)
    return key, iv


def encrypt_file(key, iv, input_file, output_file):
    with open(input_file, 'rb') as in_file:
        with open(output_file, 'wb') as out_file:
            encryptor = Cipher(algorithms.AES(key), modes.CTR(iv), backend=default_backend()).encryptor()

            while True:
                chunk = in_file.read(1024)
                if not chunk:
                    break
                encrypted_chunk = encryptor.update(chunk)
                out_file.write(encrypted_chunk)

            # Write the remaining counter value
            counter_value = encryptor.finalize()
            out_file.write(counter_value)


def decrypt_file(key, iv, input_file_path, output_file_path):
    with open(input_file_path, 'rb') as input_file, open(output_file_path, 'wb') as output_file:
        # Create the AES CTR cipher
        cipher = Cipher(algorithms.AES(key), modes.CTR(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        # Read the counter value from the end of the input file
        input_file.seek(-16, os.SEEK_END)
        counter_value = input_file.read(16)
        input_file.seek(0)
        # Decrypt the input file and write the output to the output file
        while True:
            chunk = input_file.read(1024)
            if not chunk:
                break
            decrypted_chunk = decryptor.update(chunk)
            output_file.write(decrypted_chunk)

        # Write the remaining counter value
        output_file.write(decryptor.finalize())


# Set the key length
key_length = 32
# Generate a random key and IV
key, iv = generate_key_and_iv(key_length)

# Encrypt the input file and write the output to the output file
# 開始測量
start = time.time()

# 要測量的程式碼
for i in range(10000):
    "-".join(str(n) for n in range(100))
encrypt_file(key, iv, 'input.txt', 'output_ctr.bin')
# 結束測量
end = time.time()

# 輸出結果
print("執行時間：%f 秒" % (end - start))
# Decrypt the output file and write the answer to the answer file
decrypt_file(key, iv, 'output_ctr.bin', 'answer_ctr.txt')
