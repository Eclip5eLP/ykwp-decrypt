import sys, os
sys.path.append('./lib')
from aes import decrypt_file, create_hex_table

def main():
	if not len(sys.argv) == 2:
		print("Syntax:\nfindAesKey.py <file>")
		return False
	file = sys.argv[1]
	if not os.path.isfile(file):
		print("File does not exist")
		return False
	
	success = decryptLibAll(file)
	if not success:
		print("No Key found")
		return False
	return True

def decryptLibAll(file):
	libs = ["libapminsighta.so", "libapminsightb.so", "libdiresu.so", "libEncryptorP.so", "libloader.so", "libPglmetasec_ov.so", "libSGF.so"]
	for lib in libs:
		key_path = "./lib/" + lib
		print("Testing " + lib)

		result = create_hex_table(key_path)
		keys = result
		for i, key_hex in enumerate(keys, 1):
			output_file = f"{key_hex}.json"
			success = decrypt_file(file, output_file, key_hex)
			if i % 1000 == 0:
				progress2 = (i / len(keys)) * 100
				print(f"{progress2:.3f}%", end='\r')
			if success:
				print(f"Key found: {key_hex}")
				return True
	return False

if __name__ == "__main__":
	main()