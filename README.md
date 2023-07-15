# Yokai Watch Puni Puni Decryptor

## ykwp.py
Decrypts and Encrypts ykwp files.<br>
Supported filetypes are ```.cud```, ```.m4```, ```.og```, ```.ayd```, ```.ejs```, ```.ez```, ```.ojk```<br>
<br>Syntax: ```ykwp.py <-e/-d> <file/folder>```<br>
Example:
```
ykwp.py -d "ywp_file.cud"
ykwp.py -e "ywp_file.json"
```

## yokai.exe
C/C++ and exe version of ykwp.py<br>
Only able to decrypt but fastest output.<br>
<br>Syntax:
```yokai.exe <file>```<br>
Example:
```
yokai.exe "ywp_file.cud"
yokai.exe "ywp_file.m4"
```

## findAesKey.py
Finds the AES decryption key for a given file by searching the library files.<br>
<br>Syntax: ```findAesKey.py <file>```<br>
Example:
```
findAesKey.py "ywp_file.cud"
findAesKey.py "ywp_file.ejs"
```
