import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog


class CalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("電卓アプリ")
        self.geometry("310x550")

        self.state = 0

        # メインフレーム
        main_frame = tk.Frame(self)
        main_frame.pack()

        self.result_var = tk.StringVar()
        self.result_var.set("0")
        self.expression = ""

        self.create_widgets(main_frame)
        self.create_menu()

        self.history = []
        self.history_limit = 10

    def create_widgets(self, parent_frame):
        display = tk.Entry(
            parent_frame,
            textvariable=self.result_var,
            font=("Helvetica", 20),
            justify="right",
        )
        display.grid(row=0, column=0, columnspan=4, sticky="news")

        frame2 = tk.Frame(self, width=200, height=100)
        frame2.pack()

        self.label_title = tk.Label(frame2, text="----BMIの計算画面----")
        self.label_title.pack(padx=10, pady=10)

        self.label1 = tk.Label(frame2, text="身長(cm):")
        # self.label1.grid(row=0, column=0, padx=10, pady=10)
        self.label1.pack(pady=5)

        self.height_entry = tk.Entry(frame2, font=("Arial", 15))
        # self.height_entry.grid(row=0, column=1, padx=10, pady=10)
        self.height_entry.pack(padx=5, pady=10)

        self.label2 = tk.Label(frame2, text="体重(kg):")
        # self.label2.grid(row=1, column=0, padx=10, pady=10)
        self.label2.pack()

        self.weight_entry = tk.Entry(frame2, font=("Arial", 15))
        # self.weight_entry.grid(row=1, column=1, padx=10, pady=10)
        self.weight_entry.pack(padx=5, pady=10)

        self.button = tk.Button(frame2, text="計算", command=self.calculate_bmi)
        # self.button.grid(row=2, columnspan=2, padx=10, pady=10)
        self.button.pack(padx=5, pady=10, side=tk.LEFT)

        self.result_label = tk.Label(frame2, text="BMIを表示", font=("meirio", 10))
        # self.result_label.grid(row=3, columnspan=2, padx=10)
        self.result_label.pack(padx=10, pady=10)

        self.bmi_result = tk.Label(frame2, text = "判別",font = ("meirio",10))
        self.bmi_result.pack(padx =10 ,pady =10 )
        
        button_grid = [
            ("7", 1, 0),
            ("8", 1, 1),
            ("9", 1, 2),
            ("/", 1, 3),
            ("4", 2, 0),
            ("5", 2, 1),
            ("6", 2, 2),
            ("*", 2, 3),
            ("1", 3, 0),
            ("2", 3, 1),
            ("3", 3, 2),
            ("-", 3, 3),
            ("0", 4, 0),
            (".", 4, 1),
            ("+", 4, 3),
            ("(", 5, 0),
            (")", 5, 1),
            ("=", 5, 2),
        ]

        for text, row, col in button_grid:
            button = tk.Button(
                parent_frame, text=text, command=lambda t=text: self.on_button_click(t)
            )
            button.grid(row=row, column=col, sticky="nsew")

        clear_button = tk.Button(parent_frame, text="C", command=self.clear)
        clear_button.grid(row=4, column=2, sticky="nsew")

        # Change the grid() call for the "=" button to span 2 columns
        equal_button = tk.Button(
            parent_frame, text="=", command=lambda: self.on_button_click("=")
        )
        equal_button.grid(row=5, column=2, columnspan=2, sticky="nsew")

        history_frame = tk.Frame(parent_frame)

        self.history_listbox = tk.Listbox(history_frame, height=5, selectmode=tk.SINGLE)
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        scrollbar = tk.Scrollbar(history_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.history_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.history_listbox.yview)
        history_frame.grid(row=6, column=0, columnspan=4, sticky="nsew")

    def create_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        rounding_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="端数計算", menu=rounding_menu)
        rounding_menu.add_command(label="切り捨て", command=lambda: self.rounding("切り捨て"))
        rounding_menu.add_command(label="四捨五入", command=lambda: self.rounding("四捨五入"))
        rounding_menu.add_command(label="切り上げ", command=lambda: self.rounding("切り上げ"))

        tax_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="税込計算", menu=tax_menu)
        tax_menu.add_command(label="税抜価格から税込価格を計算", command=self.calculate_tax_included)
        tax_menu.add_command(label="税込価格から税抜価格を計算", command=self.calculate_tax_excluded)

    def on_button_click(self, value):
        if value == "=":
            try:
                result = str(eval(self.expression))
                calculation = f"{self.expression} = {result}"
                self.history.append(calculation)
                if len(self.history) > self.history_limit:
                    self.history.pop(0)
                self.expression = result
            except Exception as e:
                messagebox.showerror("エラー", "計算エラー: " + str(e))
                self.expression = ""

            self.show_history()
        else:
            self.expression += value
        self.result_var.set(self.expression)

    def clear(self):
        self.expression = ""
        self.result_var.set("0")

    def rounding(self, method):
        try:
            value = float(self.expression)
            if method == "切り捨て":
                result = int(value)
            elif method == "四捨五入":
                result = round(value)
            elif method == "切り上げ":
                if value < 1:
                    result = 1
                else:
                    result = -int(-value)
            else:
                return
            self.expression = str(result)
            self.result_var.set(self.expression)
        except ValueError:
            messagebox.showerror("エラー", "有効な数値を入力してください")

    def calculate_tax_included(self):
        try:
            value = float(self.expression)
            result = value * 1.1
            result = -int(-result)
            self.expression = str(result)
            self.result_var.set(self.expression)
        except ValueError:
            messagebox.showerror("エラー", "有効な数値を入力してください")

    def calculate_tax_excluded(self):
        try:
            value = float(self.expression)
            result = value / 1.1
            result = -int(-result)
            self.expression = str(result)
            self.result_var.set(self.expression)
        except ValueError:
            messagebox.showerror("エラー", "有効な数値を入力してください")

    def calculate_bmi(self):
        if not self.weight_entry.get() and not self.height_entry.get():
            messagebox.showerror("エラー", "体重と身長の両方を入力してください")
            return

        if not self.weight_entry.get():
            messagebox.showerror("エラー", "体重を入力してください")
            return

        if not self.height_entry.get():
            messagebox.showerror("エラー", "身長を入力してください")
            return

        height_cm = float(self.height_entry.get())
        weight = float(self.weight_entry.get())

        height_m = height_cm / 100
        bmi = weight / (height_m**2)

        bmi_str = format(bmi, ".2f")
        self.result_label.config(text=f"BMI: {bmi_str}")

takeru556
        self.height_entry.delete(0, 'end')
        self.weight_entry.delete(0, 'end')
        
        try:
            bmi = float(bmi_str)
            if bmi > 30:
                self.bmi_result.config(text="高度肥満です")
            elif bmi > 25:
                self.bmi_result.config(text="肥満です")
            elif bmi > 18.5:
                self.bmi_result.config(text="普通体重です")
            else:
                self.bmi_result.config(text="やせ型です")
        
        except ValueError:
            messagebox.showerror("エラー", "BMIの値が不正です")
        

        self.height_entry.delete(0, "end")
        self.weight_entry.delete(0, "end")

main
    def show_history(self):
        self.history_listbox.delete(0, tk.END)
        for item in self.history:
            self.history_listbox.insert(tk.END, item)

        if not self.history:
            self.history_listbox.insert(tk.END, "履歴は空です")


if __name__ == "__main__":
    app = CalculatorApp()
    app.mainloop()
