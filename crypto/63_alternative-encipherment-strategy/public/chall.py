import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


if __name__ == "__main__":
    key = os.urandom(16)
    iv1 = os.urandom(16)
    iv2 = os.urandom(16)

    print("iv1:", iv1.hex())
    print("iv2:", iv2.hex())

    cipher1 = AES.new(key, AES.MODE_CBC, iv1)
    plaintext1 = bytes.fromhex(input("Enter the message to encrypt (in hex): "))
    ciphertext1 = cipher1.encrypt(pad(plaintext1, 16))
    print("ciphertext1:", ciphertext1.hex())

    # I don't like to reuse things, including ivs and encryption modes
    # But it does not make sense to change my key everytime I use it, right?
    # Just like you won't change your password everytime you log in!
    cipher2 = AES.new(key, AES.MODE_OFB, iv2)
    ciphertext2 = bytes.fromhex(input("Enter a ciphertext (in hex):"))

    try:
        plaintext2 = unpad(cipher2.decrypt(ciphertext2), 16)
    except:
        plaintext2 = b""
    if plaintext2 == b"Please give me the flag! UwU!":
        try:
            with open("flag.txt", "rb") as f:
                flag = f.read()
        except:
            # Do not submit. This is not the real flag.
            flag = b"cuhk24ctf{this_is_a_test_flag}"
        print("Here is the flag:", flag.decode())
    else:
        print("HTTP/1.1 400 Bad Request")
