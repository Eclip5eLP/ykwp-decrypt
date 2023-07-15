import sys, os
import binascii
import json
sys.path.append('./lib')
from aes import decrypt_file, encrypt_file, create_hex_table

def loadKeys():
	with open('./lib/keys.json', 'r') as f:
		keys = json.load(f)
	return keys

def main(file, mode):
	ftype = -1
	if os.path.isdir(file):
		ftype = 0
	elif os.path.isfile(file):
		ftype = 1
	else:
		print("File not found")
		return False

	r = -1
	if ftype == 0: # Directory
		for f in os.listdir(file):
			r = crypt(file + f, mode)
		print("Done")
		return r
	elif ftype == 1: # Single file
		r = crypt(file, mode)
		print("Done")
		return r

def crypt(file, mode):
	fname, file_extension = os.path.splitext(file)
	keys = loadKeys()

	# Check extension
	key = None
	target = None
	for ext in keys["ext"]:
		if "." + ext[(1 if mode == "-e" else 0)] == file_extension:
			key = keys["keys"][ext[2]]
			target = ext[(0 if mode == "-e" else 1)]
			break

	if key == None or target == None:
		return False

	print(file)
	if mode == "-e": # Encrypt
		return encrypt_file(file, fname + "." + target, key)
	elif mode == "-d": # Decrypt
		return decrypt_file(file, fname + "." + target, key)

	# if mode == "-e": # Encrypt
	# 	if file_extension != ".json":
	# 		return False
	# 	print(file)
	# 	return encrypt_file(file, fname + ".cud", key)
	# elif mode == "-d": # Decrypt
	# 	if file_extension != ".cud":
	# 		return False
	# 	print(file)
	# 	return decrypt_file(file, fname + ".json", key)

if __name__ == "__main__":
	if (len(sys.argv) != 3) or (sys.argv[1] != "-e" and sys.argv[1] != "-d"):
		print("Syntax:\n" + os.path.basename(sys.argv[0]) + " <-e/-d> <file/folder>")
		exit()

	main(sys.argv[2], sys.argv[1])