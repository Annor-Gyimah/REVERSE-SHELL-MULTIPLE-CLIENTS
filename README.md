
# REVERSE SHELL MULTIPLE CLIENTS


## Description
* Gain access to a remote machine using reverse shell in python. This reverse shell is able to accept
multiple clients and allows the server to select a client to connect to and control it.


## Installation
For this to work you should have python installed.
For installation open git bash if on windows to simply clone it.

git clone https://github.com/Annor-Gyimah/REVERSE-SHELL-MULTIPLE-CLIENTS.git
* First open the CMD and run "pip install -r requirements.txt"
e.g. pip install -r requirements.txt

## Usage
* The server.py file should be installed on the attacker
machine while the client.py runs on the target(victim) machine
* On the windows terminal, run "python server.py"
e.g. python server.py
* Make sure the clients.py have the same ip address and port number as the server.py
* If python is installed you, open the client.py with your favourite text editor then compile it with python or
you can open the windows CMD as well then you run "python client.py"


## Functionalities
* Downloading files from selected client's machine with progress bar displayed.

* Uploading files from server to client's machine with progress bar displayed.

* Screenshoting client's screen and sending it over to the server.

* Recording client's audio by the number of seconds specified by the attacker on the server side.

* Capturing client's webcam and sending it over to the server.

* Extraction of Google saved passwords from the client's machine and sending it over to the attacker. 
This saves the passwords in a file with the client's username and this helps to differentiate saved passwords from different targert's or victims.

* Encryption of files on the client's machine and sending the salt file over to the server or attacker's side and deleting it from the client's side.
The salt file is then saved as the encrypted filename.salt. This is to differentiate the many salts that will be generated for different files encrypted.
Also the encrypted filename.txt will be generated which gives a notice to the client that his/her file is encrypted. This is custom and can be changed in the client.py

* Decryption of the files back on the client's machine. 
The decryption only happens after the attacker sends the encrypted file's generated salt file back to the client's machine.

* Extract Wi-Fi saved connections' passwords on the client's machine and send it over to the server.
The file sent to the server contains the WI-FI's name and the saved passwords. The saved passwords will be in a file called the client's computer.
username-wifi.txt. This again is to differentiate saved WI-FI's passwords from different clients.

* Deletion of files from the client's machine.

* Opening of websites on the client's machine.


## Contributions
Any contributions or changes are highly welcomed<br>Folk the repo and perform the changes you deem necessary then do a pull requests 
and your changes will be incorporated.<br>Any issues raised will also be looked into.

## Author
Annor Gyimah

##### This script is for education purpose only am not liable for any damages