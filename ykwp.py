import sys, os
import binascii
sys.path.append('./lib')
from aes import decrypt_file, encrypt_file, create_hex_table

def main(file, mode):
	ftype = -1
	if os.path.isdir(file):
		ftype = 0
	elif os.path.isfile(file):
		ftype = 1
	else:
		print("File not found")
		return False

	key = binascii.unhexlify("A33C778C0A625BEC694310C2FE215629").hex()

	r = -1
	if ftype == 0: # Directory
		for f in os.listdir(file):
			r = crypt(file + f, mode, key)
		print("Done")
		return r
	elif ftype == 1: # Single file
		r = crypt(file, mode, key)
		print("Done")
		return r

def crypt(file, mode, key):
	fname, file_extension = os.path.splitext(file)
	if mode == "-e": # Encrypt
		if file_extension != ".json":
			return False
		print(file)
		return encrypt_file(file, fname + ".cud", key)
	elif mode == "-d": # Decrypt
		if file_extension != ".cud":
			return False
		print(file)
		return decrypt_file(file, fname + ".json", key)

if __name__ == "__main__":
	if (len(sys.argv) != 3) or (sys.argv[1] != "-e" and sys.argv[1] != "-d"):
		print("Syntax:\n" + os.path.basename(sys.argv[0]) + " <-e/-d> <file/folder>")
		exit()

	main(sys.argv[2], sys.argv[1])