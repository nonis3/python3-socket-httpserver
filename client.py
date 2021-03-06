#!/usr/bin/env python3
import socket
import sys
import os

MSGLEN = 1024

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("client.py server_host server_port filename")
        sys.exit()
    if len(sys.argv) == 3:
        sys.argv.append('/index.html')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((sys.argv[1], int(sys.argv[2])))
    s.send(('GET ' + sys.argv[3] + ' HTTP 1/1\r\n').encode())
    chunks = []
    bytes_recd = 0
    try:
        while bytes_recd < MSGLEN:
            chunk = s.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
    except Exception as e:
        pass
    file_name = '/' + sys.argv[3]
    if file_name[0] == '/' and file_name[1] == '/':
        file_name = file_name[1:]
    if file_name == '/':
        file_name = '/index.html'
    file_path = 'Download' + file_name
    if len(chunks) == 0 or chunks[0] == b'HTTP/1.0 404 Not Found\r\n':
        print("404 File Not Found")
    else:
        try:
            os.remove(file_path)
        except OSError:
            pass
        print('Downloading ' + file_name + ' to ' + file_path)
        with open(file_path, 'wb') as w:
            sp = b''.join(chunks).split(b'\r\n')
            try:
                file_contents = sp[5]
                try:
                    utf_contents = file_contents.decode('utf8')
                    print("Contents as utf8:")
                    print(utf_contents)
                except Exception as e:
                    print("Contents as bytes:")
                    print(file_contents)
                w.write(file_contents)
            except:
                print("403 Permission Denied")
