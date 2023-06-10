import socket
import atexit
import errno
import sys

class Communication:
    def __init__(self):
        #self.HEADER_LENGTH = 10
        self.IP = '0.0.0.0'
        self.PORT = 8080
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (self.IP, self.PORT)
        try:
            self.s.bind(server_address)
        except:
            self.s.close()

    def send(self, ip, string):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (ip, self.PORT)
        s.connect(server_address)
        try:
            s.sendall(string.encode('utf-8'))
        finally:
            s.close()
            
    def receive(self):
        self.s.listen(1)
        connection, client_address = self.s.accept()
        while(True):
            try:
                bits = connection.recv(1024).decode()
            finally:
                connection.close()
            return bits
            
            
    def get_ip_address(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip_address = ''
        try:
            s.connect(("8.8.8.8", 80))
            ip_address = s.getsockname()[0]
        except:
            s.close()
        finally:
            s.close()
        return ip_address


    def close_connection(self):
        self.s.close()