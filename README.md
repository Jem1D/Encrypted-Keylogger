# Encrypted-Keylogger
The source code is for encrypting the traditional keylogger using the Counter mode of operation in Advanced Encryption Standard.


To use the keylogger, first you need to disable the antivirus from the device as these softwares block the use of any keylogging softwares by default.

You can also turn off the windows defender(if you use it) for the particular keyloggr.py file.

Steps to log:
1) Run the keyloggr.py file in python ide or terminal.
2) Type or click anything anywhere on the PC.
3) These will be logged by the program and stored in the log.json file. This file is stores content in AES encrypted form.
4) To decrypt the logs run decrypt.py file which will print "Decrypted successfully."
5) You can see the typed or clicked events in the decrypted.txt file created.
