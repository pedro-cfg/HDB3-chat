import tkinter as tk
import numpy as np
import threading
import atexit
from Communication import Communication as conn

class App(tk.Frame):
    def build_sender_frame(self):
        frame = tk.Frame(self.content, borderwidth=2, relief='groove')
        frame.columnconfigure(0, weight = 1)
        frame.rowconfigure(0, weight = 1)
        frame.rowconfigure(1, weight = 1)
        frame.rowconfigure(2, weight = 1)
        frame.rowconfigure(3, weight = 4)
        frame.rowconfigure(4, weight = 4)
        frame.rowconfigure(5, weight = 4)
        frame.rowconfigure(6, weight = 1)

        conn_conf = tk.Frame(frame, relief='groove')
        conn_conf.grid(row=0, column=0, sticky=(tk.W, tk.E))
        conn_conf.columnconfigure(0,weight = 1)
        conn_conf.columnconfigure(1,weight = 1)
        conn_conf.rowconfigure(0, weight = 1)
        ask_ip_text = tk.StringVar(value='Insert destiny IP address:')
        ask_ip_label = tk.Label(conn_conf, textvariable = ask_ip_text, wraplength = '200').grid(row=0, column=0, sticky=(tk.E))
        self.ip_address = tk.Entry(conn_conf, width = 30)
        self.ip_address.grid(row=0, column=1, padx=50, sticky=(tk.W))
        self.ip_address.insert(0, self.initial_ip)

        ask_for_text = tk.StringVar(value='Insert text:')
        ask_text_label = tk.Label(frame, textvariable = ask_for_text, wraplength = '200').grid(row=1, column=0, sticky=(tk.W, tk.E))

        self.data_entry = tk.Entry(frame, width = 30)
        self.data_entry.insert(0, self.text)

        self.crypt_label = tk.Label(frame, textvariable = self.crypt_string, wraplength = '500')
        self.bit_label = tk.Label(frame, textvariable = self.bit_string, width = 30, wraplength = '500')
        self.hdb3_label = tk.Label(frame, textvariable = self.hdb3_string, width = 30, wraplength = '500')

        self.data_entry.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N))
        self.crypt_label.grid(row=3, column=0, sticky=(tk.W, tk.E))
        self.bit_label.grid(row=4, column=0, sticky=(tk.W, tk.E))
        self.hdb3_label.grid(row=5, column=0, sticky=(tk.W, tk.E))
        
        self.send_button = tk.Button(frame, text = 'Send', command = self.on_send).grid(row=6, column=0, padx=200, sticky=(tk.W, tk.E))

        return frame

    def build_receiver_frame(self):
        frame = tk.Frame(self.content, borderwidth=2, relief='groove')
        frame.columnconfigure(0, weight = 1)
        frame.rowconfigure(0, weight = 1)
        frame.rowconfigure(1, weight = 1)
        frame.rowconfigure(2, weight = 4)
        frame.rowconfigure(3, weight = 4)
        frame.rowconfigure(4, weight = 4)

        self.data_out = tk.Label(frame, textvariable = self.data_string, width = 30)
        self.decrypt_label = tk.Label(frame, textvariable = self.decrypt_string, width = 30, wraplength = '500')
        self.debit_label = tk.Label(frame, textvariable = self.debit_string, width = 30, wraplength = '500')
        self.dehdb3_label = tk.Label(frame, textvariable = self.dehdb3_string, width = 30, wraplength = '500')
        
        font = ("Arial", 20) 
        self.data_out['font'] = font

        myIP = tk.Frame(frame, relief='groove')
        myIP.grid(row=0, column=0, sticky=(tk.W, tk.E))
        myIP.columnconfigure(0,weight = 1)
        myIP.columnconfigure(1,weight = 1)
        myIP.rowconfigure(0, weight = 1)
        show_ip_text = tk.StringVar(value='My IP Address:')
        show_ip_label = tk.Label(myIP, textvariable = show_ip_text, wraplength = '200').grid(row=0, column=0, sticky=(tk.E))
        ip_label = tk.Label(myIP, textvariable = self.my_ip, wraplength = '200')
        ip_label.grid(row=0, column=1, sticky=(tk.W))

        self.data_out.grid(row=1, column=0, sticky=(tk.W, tk.E))
        self.decrypt_label.grid(row=2, column=0, sticky=(tk.W, tk.E))
        self.debit_label.grid(row=3, column=0, sticky=(tk.W, tk.E))
        self.dehdb3_label.grid(row=4, column=0, sticky=(tk.W, tk.E))

        return frame

    def build_plot(self):
        from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
        from matplotlib.figure import Figure

        fig = Figure(figsize=(100, 1.6), tight_layout=True)
        self.ax = fig.add_subplot()

        frame = tk.Frame(self, borderwidth=2, relief='groove')
        self.canvas = FigureCanvasTkAgg(fig, master=frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        self.canvas.draw()

        return frame

    def update_plot(self, t, x):
        import numpy as np
        self.ax.clear()

        self.ax.set_xticks(np.arange(0, t[-1]+1, 1))
        self.ax.set_yticks([0])
        self.ax.tick_params(length = 0, labelsize = 0)
        self.ax.grid(True, linestyle='--')
        self.ax.set_frame_on(False)

        self.ax.step(t, x, where='post')
        self.canvas.draw()


    def __init__(self, master=None):
        super().__init__(master)
        
        self.initial_ip = '127.0.0.1'
        self.text = 'こんにちは'
        self.crypt_string = tk.StringVar(value='*****')
        self.bit_string = tk.StringVar(value='-----')
        self.hdb3_string = tk.StringVar(value='-----')
        self.data_string = tk.StringVar(value='null')
        self.decrypt_string = tk.StringVar(value='*****')
        self.debit_string = tk.StringVar(value='-----')
        self.dehdb3_string = tk.StringVar(value='-----')
        
        self.c = conn()
        self.receive_active = False
        self.receiver_thread = None
        self.my_ip = tk.StringVar(value=self.c.get_ip_address())
        
        self.button_frame = tk.Frame(self)
        self.button_frame.pack()

        self.content = tk.Frame(self);
        self.content.pack(fill='both', expand=True);
        
        sender_button = tk.Button(self.button_frame, text='Sender', command=self.show_sender)
        sender_button.pack(side='left', padx=10, pady=10, anchor='center')

        receiver_button = tk.Button(self.button_frame, text='Receiver', command=self.show_receiver)
        receiver_button.pack(side='left', padx=10, pady=10, anchor='center')
        
        self.show_receiver()
        self.show_sender()
        
        self.master.title('Comunicação de dados')
        self.master.geometry('800x800')
        self.bind_all('<Return>', lambda e: self.on_send())
        self.pack(fill='both', expand=True)

        self.build_plot().pack(fill='both')
        self.update_plot([0], [0])
        
        atexit.register(self.c.close_connection)

    def show_sender(self):
        for child in self.content.winfo_children():
           child.destroy()
        self.build_sender_frame().pack(fill='both', expand=True)

    def show_receiver(self):
        for child in self.content.winfo_children():
          child.destroy()
        self.build_receiver_frame().pack(fill='both', expand=True)
        self.start_receiver_thread()

    def on_send(self):
        ip = bytearray(self.ip_address.get(), 'utf-8')
        self.initial_ip = self.ip_address.get();
        self.text = self.data_entry.get()
        plaintext = bytearray(self.data_entry.get(), 'utf-8')
        ciphertext = bytearray([255-x for x in plaintext])
        bit_string = ''.join(format(x, '08b') for x in ciphertext);
        #bit_string = '1100001000000000'                                                                                #Código do PDF pra exemplificar a codificação
        hdb3 = ''.join(str(x) for x in self.hdb3_encode(bit_string));

        self.crypt_string.set(ciphertext.hex())
        self.bit_string.set(bit_string)
        self.hdb3_string.set(hdb3)
        
        self.c.send(ip,hdb3)

        t = np.arange(0, len(hdb3)+1)
        x = []
        for c in hdb3:
            if c == '+':
                x.append(1)
            elif c == '-':
                x.append(-1)
            else:
                x.append(0)
        x.append(x[-1])
        self.update_plot(t, x)
    
    def start_receiver_thread(self):
        if self.receiver_thread is None or not self.receiver_thread.is_alive():
            self.receive_active = True
            self.receiver_thread = threading.Thread(target=self.receive_code)
            self.receiver_thread.daemon = True
            self.receiver_thread.start()
    
    def receive_code(self):
        while self.receive_active:
            bits = self.c.receive()
            self.process_received_code(bits)
        
    def process_received_code(self, code):
        self.dehdb3_string.set(code)
        bits = ''.join(str(x) for x in self.hdb3_decode(code));
        self.debit_string.set(bits)
        bit_groups = [bits[i:i+4] for i in range(0, len(bits), 4)]
        hex_string = ''.join(format(int(bits, 2), 'x') for bits in bit_groups)
        byte_array = bytes.fromhex(hex_string)
        self.decrypt_string.set(byte_array.hex())
        try:
            self.data_string.set(bytearray([255-x for x in byte_array]).decode('utf-8'))  
        except UnicodeDecodeError:
            print()
        
        t = np.arange(0, len(code)+1)
        x = []
        for c in code:
            if c == '+':
                x.append(1)
            elif c == '-':
                x.append(-1)
            else:
                x.append(0)
        x.append(x[-1])
        self.update_plot(t, x)
    
    def hdb3_encode(self, bits):
        encoded_bits = []
        last_polarity = '-'
        one_parity = 0
        consecutive_zeros = 0

        for bit in bits:
            if bit == '1':
                consecutive_zeros = 0
                one_parity = (one_parity + 1) % 2
                if last_polarity == '+':
                    encoded_bits.append('-')
                    last_polarity = '-'
                else:
                    encoded_bits.append('+')
                    last_polarity = '+'
            else:  
                consecutive_zeros += 1

                if consecutive_zeros == 4:
                    if one_parity == 1:
                        if last_polarity == '+':
                            encoded_bits.append('+')
                        else:
                            encoded_bits.append('-')
                    else:
                        if last_polarity == '+':
                            encoded_bits.pop()
                            encoded_bits.pop()
                            encoded_bits.pop()
                            encoded_bits.extend(['-', '0', '0', '-'])
                            last_polarity = '-'
                        else:
                            encoded_bits.pop()
                            encoded_bits.pop()
                            encoded_bits.pop()
                            encoded_bits.extend(['+', '0', '0', '+'])
                            last_polarity = '+'
                    one_parity = 0;
                    consecutive_zeros = 0
                else:
                    encoded_bits.append('0')

        return encoded_bits      

    def hdb3_decode(self, code):
        decoded_bits = []
        last_polarity = ''
        for signal in code:
            if signal == '0':
                decoded_bits.append('0')
            else:
                if last_polarity == signal:
                    decoded_bits.pop()
                    decoded_bits.pop()
                    decoded_bits.pop()
                    decoded_bits.extend(['0', '0', '0', '0'])
                else:
                    last_polarity = signal
                    decoded_bits.append('1')
        return decoded_bits

        
myapp = App()
myapp.mainloop()
