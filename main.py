import tkinter as tk

text = 'こんにちは'

class App(tk.Frame):
    def build_sender_frame(self):
        frame = tk.Frame(self, borderwidth=2, relief='groove')
        frame.columnconfigure(0, weight = 1)
        frame.rowconfigure(0, weight = 1)
        frame.rowconfigure(1, weight = 4)
        frame.rowconfigure(2, weight = 4)

        self.data_entry = tk.Entry(frame, width = 30)
        self.data_entry.insert(0, text)

        self.crypt_string = tk.StringVar(value='*****')
        self.crypt_label = tk.Label(frame, textvariable = self.crypt_string, wraplength = '300')

        self.bit_string = tk.StringVar(value='-----')
        self.bit_label = tk.Label(frame, textvariable = self.bit_string, width = 30, wraplength = '300')

        self.data_entry.grid(row=0, column=0, sticky=(tk.W, tk.E))
        self.crypt_label.grid(row=1, column=0, sticky=(tk.W, tk.E))
        self.bit_label.grid(row=2, column=0, sticky=(tk.W, tk.E))

        return frame

    def build_receiver_frame(self):
        frame = tk.Frame(self, borderwidth=2, relief='groove')
        frame.columnconfigure(0, weight = 1)
        frame.rowconfigure(0, weight = 1)
        frame.rowconfigure(1, weight = 4)
        frame.rowconfigure(2, weight = 4)

        self.data_string = tk.StringVar(value='null')
        self.data_out = tk.Label(frame, textvariable = self.data_string, width = 30)

        self.decrypt_string = tk.StringVar(value='*****')
        self.decrypt_label = tk.Label(frame, textvariable = self.decrypt_string, width = 30, wraplength = '300')

        self.debit_string = tk.StringVar(value='-----')
        self.debit_label = tk.Label(frame, textvariable = self.debit_string, width = 30, wraplength = '300')

        self.data_out.grid(row=0, column=0, sticky=(tk.W, tk.E))
        self.decrypt_label.grid(row=1, column=0, sticky=(tk.W, tk.E))
        self.debit_label.grid(row=2, column=0, sticky=(tk.W, tk.E))

        return frame

    def build_plot(self):
        from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
        from matplotlib.figure import Figure

        fig = Figure(figsize=(100, 1), tight_layout=True)
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
        self.master.title('Comunicação de dados')
        self.master.geometry('800x400')
        self.bind_all('<Return>', lambda e: self.on_send())
        self.pack(fill='both', expand=True)

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
        self.rowconfigure(0, weight = 9)
        self.rowconfigure(1, weight = 5)
        self.rowconfigure(2, weight = 1)
        self.grid_propagate(0)

        self.build_sender_frame().grid(column = 0, row = 0, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.build_receiver_frame().grid(column = 1, row = 0, sticky=(tk.N, tk.S, tk.W, tk.E))

        self.build_plot().grid(column = 0, columnspan = 2, row = 1, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.update_plot([0], [0])

        tk.Button(self, text = 'Send', command = self.on_send).grid(row=2, column=0, columnspan=2, sticky=(tk.N, tk.E, tk.W, tk.S))

    def on_send(self):
        plaintext = bytearray(self.data_entry.get(), 'utf-8')
        ciphertext = bytearray([255-x for x in plaintext])
        bit_string = ''.join(format(x, '08b') for x in plaintext);

        self.crypt_string.set(ciphertext.hex())
        self.bit_string.set(bit_string)

        self.debit_string.set(self.bit_string.get())
        self.decrypt_string.set(ciphertext.hex())
        self.data_string.set(bytearray([255-x for x in ciphertext]).decode())

        import numpy as np
        t = np.arange(0, len(bit_string)+1)
        x = [1 if c == '1' else 0 for c in bit_string]
        x.append(x[-1])
        self.update_plot(t, x)

myapp = App()
myapp.mainloop()
