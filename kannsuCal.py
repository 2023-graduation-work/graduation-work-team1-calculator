import tkinter as tk
from math import *

memory = 0

def calculate():
    global memory
    try:
        result = eval(entry.get())
        history.insert(tk.END, entry.get() + " = " + str(result))
        entry.delete(0, tk.END)
        entry.insert(tk.END, str(result))
        memory = result
    except:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "無効な入力")

def clear():
    entry.delete(0, tk.END)

def recall_memory():
    entry.delete(0, tk.END)
    entry.insert(tk.END, str(memory))

def calculate():
    try:
        result = eval(entry.get())
        history.insert(tk.END, entry.get() + " = " + str(result))
        entry.delete(0, tk.END)
        entry.insert(tk.END, str(result))
    except:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "無効な入力")

def clear():
    entry.delete(0, tk.END)

self = tk.Tk()
self.title("高度な電卓")
self.geometry("1200x800")



entry = tk.Entry(self, width=45,font=('Helvetica', 30))
entry.grid(row=0, column=0, columnspan=4,padx=5,pady=5)

buttons = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    '0', '.', '=', '+'
]

function_buttons = [
    tk.Button(self, text=func, width=10, height=2, font=('Helvetica', 10), command=lambda func=func: entry.insert(tk.END, " " + func + "() "))
    for func in ['sin', 'cos', 'tan', 'log', 'sqrt']
]
recall_button = tk.Button(self, text="Recall", width=10, height=2, font=('Helvetica', 10), command=recall_memory)
recall_button.grid(row=6,column=4,padx=5, pady=5)


row_val = 1
col_val = 0

for button in buttons:
    if button == '=':
        btn = tk.Button(self, text=button, width=10, height=2, font=('Helvetica', 20), command=calculate)
        btn.grid(row=row_val, column=col_val, padx=1, pady=1)
    elif button in '0123456789.':
        btn = tk.Button(self, text=button, width=10, height=2, font=('Helvetica', 20), command=lambda button=button: entry.insert(tk.END, button))
        btn.grid(row=row_val, column=col_val, padx=5, pady=5)
    else:
        btn = tk.Button(self, text=button, width=10, height=2, font=('Helvetica', 20), command=lambda button=button: entry.insert(tk.END, " " + button + " "))
        btn.grid(row=row_val, column=col_val, padx=5, pady=5)

    col_val += 1
    if col_val > 3:
        col_val = 0
        row_val += 1

for i in range(5):
    function_buttons[i].grid(row=i+1,column=4,padx=5, pady=5)

clear_button = tk.Button(self,text='C',width = 10,height = 2 ,font=('Helvetica',20),command = clear)
clear_button.grid(row=row_val,column = col_val)

history_frame = tk.Listbox(self, width=40, height=5,font=('Helvetica',20) )

history_frame.grid(row=row_val, columnspan=6)

scrollbar = tk.Scrollbar(history_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

history = tk.Listbox(history_frame,width=40, height=5,font=('Helvetica',15) )
history.pack(side=tk.LEFT)

history.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=history.yview)

self.mainloop()

