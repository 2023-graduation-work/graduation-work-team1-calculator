import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog


class CalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("電卓アプリ")
        self.geometry("300x400")

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

        display = tk.Entry(parent_frame, textvariable=self.result_var, font=("Helvetica", 20), justify="right")
        display.grid(row=0, column=0, columnspan=4, sticky="news")

        # 2つ目のフレーム
        frame2 = tk.Frame(self, width=200, height=100)
        frame2.pack()  # pack frame2 into the main frame

        button_grid = [
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
            ("0", 4, 0), (".", 4, 1), ("+", 4, 3),
            ("(", 5, 0), (")", 5, 1), ("=", 5, 2)
        ]

        for (text, row, col) in button_grid:
            button = tk.Button(parent_frame, text=text, command=lambda t=text: self.on_button_click(t))
            button.grid(row=row, column=col, sticky="nsew")

        clear_button = tk.Button(parent_frame, text="C", command=self.clear)
        clear_button.grid(row=4, column=2,  sticky="nsew")

        # Change the grid() call for the "=" button to span 2 columns
        equal_button = tk.Button(parent_frame, text="=", command=lambda: self.on_button_click("="))
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

        bmi_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="BMI計算", menu=bmi_menu)
        bmi_menu.add_command(label="BMIを計算", command=self.calculate_bmi)

        history_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="履歴", menu=history_menu)
        history_menu.add_command(label="履歴を表示", command=self.show_history)

    def on_button_click(self, value):
        if value == "=":
            try:
                result = str(eval(self.expression))
                calculation = f"{self.expression} = {result}"
                self.history.append(calculation)
                if len(self.history) > self.history_limit:
                    self.history.pop(0)  # 履歴の上限を制限
                self.expression = result
            except Exception as e:
                messagebox.showerror("エラー", "計算エラー: " + str(e))
                self.expression = ""
            # リストボックスに履歴を表示
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
            result = -int(-result)  # Round up to the nearest whole number
            self.expression = str(result)
            self.result_var.set(self.expression)
        except ValueError:
            messagebox.showerror("エラー", "有効な数値を入力してください")

    def calculate_tax_excluded(self):
        try:
            value = float(self.expression)
            result = value / 1.1
            result = -int(-result)  # Round up to the nearest whole number
            self.expression = str(result)
            self.result_var.set(self.expression)
        except ValueError:
            messagebox.showerror("エラー", "有効な数値を入力してください")

    def calculate_bmi(self):

        details = simpledialog.askstring("BMI計算", "体重(kg)と身長(cm)をカンマで区切って入力してください(例:60,170)")

        if details:
            weight, height_cm = map(float, details.split(','))
            height_m = height_cm / 100
            bmi = weight / (height_m ** 2)
            messagebox.showinfo("BMI計算結果", f"BMI: {bmi:.2f}")

    def show_history(self):
        self.history_listbox.delete(0, tk.END)
        for item in self.history:
            self.history_listbox.insert(tk.END, item)

        if not self.history:
            self.history_listbox.insert(tk.END, "履歴は空です")

if __name__ == "__main__":
    app = CalculatorApp()
    app.mainloop()

