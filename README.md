# Yokai Watch Puni Puni Decryptor

## yokai.exe
Decrypts multiple encrypted file types.<br>
Supported filetypes are ```.cud```, ```.m4```, ```.og```, ```.ayd```, ```.ejs```<br>
<br>Syntax:
```yokai.exe <file>```<br>
Example:
```
yokai.exe "ywp_file.cud"
yokai.exe "ywp_file.m4"
```

## ykwp.py
Decrypts and Encrypts ```.cud``` files.<br>
Encryption mode needs an original encrypted file to work.<br>
<br>Syntax: ```ykwp.py <-e/-d> <file/folder>```<br>
Example:
```
ykwp.py -d "ywp_file.cud"
ykwp.py -e "ywp_file.json"
```

## findAesKey.py
Finds the AES decryption key for a given file by searching the library files.<br>
<br>Syntax: ```findAesKey.py <file>```<br>
Example:
```
findAesKey.py "ywp_file.cud"
findAesKey.py "ywp_file.ejs"
```
