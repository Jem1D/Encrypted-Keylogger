# imports 

import sys
from Crypto.Cipher import AES
from key_iv import key
import json
from base64 import b64decode


class Decryption:

    def __init__(self,filename):
        self.filename = filename

    def decryption(self):	# produces the original result
        try:
            encrypted_file_object = open(self.filename,'r')
        except (FileNotFoundError,IOError):
            print('File with name {} is not found'.format(self.filename))
            sys.exit(0)
        try:
            # decrypted_file = input('Enter the filename for the Decryption file with extension:') # Decrypted file as output

            decrypted_file_object = open("decrypted.txt",'ab')
            
            cipher_text = encrypted_file_object.read()

            b64 = json.loads(cipher_text)
            for i in range(len(b64)):
                nonce = b64decode(b64[i]['nonce'])
                ct = b64decode(b64[i]['ciphertext'])
                cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
                pt = cipher.decrypt(ct)
                decrypted_file_object.write(b"\n"+pt+b"\n")
			
            print('Decryption is done Sucessfully...!')

        except Exception as e:
            print(e)

        finally:
            encrypted_file_object.close()
            decrypted_file_object.close()



print("DECRYPTION........")
# file = input()
D1 = Decryption("logs.json")
D1.decryption()


		