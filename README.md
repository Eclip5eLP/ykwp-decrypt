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

## parseCud.py
Reads a decrypted cud (.json) and parses its contents to be easier to edit.<br>
Will also reverse and merge the parsed contents with the original.<br>
<br>Syntax:
```parseCud.py <-p/-u> <file>```<br>
Example:
```
parseCud.py -p "ywp_file.json"
parseCud.py -u "ywp_file_parsed.json"
```

## findAesKey.py
Finds the AES decryption key for a given file by searching the library files.<br>
<br>Syntax: ```findAesKey.py <file>```<br>
Example:
```
findAesKey.py "ywp_file.cud"
findAesKey.py "ywp_file.ejs"
```

<br><br><hr>
Keys found by DarkCraft<br>
Scripts written by Eclip5e
