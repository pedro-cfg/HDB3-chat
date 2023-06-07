import socket
import errno
import sys

class Communication:
    def __init__(self, server_address, on_recv):
        self.HEADER_LENGTH = 10
        self.IP = server_address
        self.PORT = 8080
        self.on_recv = on_recv
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        if self.IP == '0.0.0.0':
            self.s.bind((self.IP, self.PORT))

            self.s.listen(1)
            print(f'Listening on {self.IP}')

            self.cs, add = self.s.accept()
            self.cs.setblocking(False)
            print(f'Connectioin from {add}')
        else:
            self.s.connect((self.IP, self.PORT))
            self.s.setblocking(False)
            self.cs = self.s


    def send(self, message_utf8):
        message_lenght = f"{len(message_utf8):<{self.HEADER_LENGTH}}".encode('utf-8')
        self.cs.send(message_lenght + message_utf8)

    def try_recv(self):
        try:
            while True:
                header = self.cs.recv(self.HEADER_LENGTH)
                if not len(header):
                    print('Connection closed')
                    sys.exit()

                message_lenght = int(header.decode('utf-8').strip())
                message = self.cs.recv(message_lenght).decode('utf-8')

                self.on_recv(message)
        except IOError as e:
            if e.errno == 11:
                pass
            else:
                print(e)
            pass
        except Exception as e:
            print(e)
            pass

def on_recv(message):
    print('< {}'.format(message))

conn = Communication(sys.argv[1], on_recv)
conn.connect()

while True:
    message = input('> ')
    if message:
        conn.send(message.encode('utf-8'))

    conn.try_recv()
