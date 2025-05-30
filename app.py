import tkinter as tk
import ttkbootstrap as ttk
import math
import re

root = ttk.Window(themename="darkly")
root.title("Scientific Calculator")

style = ttk.Style()

entry = tk.Entry(root,
                 width=50,
                 font=('Segoe UI', 18),
                 fg="white",
                 bg="#313030",
                 readonlybackground="#333",
                 bd=2,
                 relief="solid",
                 justify='right',
                 state="readonly")
entry.grid(row=0, column=0, columnspan=7, padx=10, pady=10)

ce_canvas_ref = None
ce_label_ref = None

def set_display(text):
    entry.config(state="normal")
    entry.delete(0, tk.END)
    entry.insert(0, text)
    entry.config(state="readonly")

def button_click(value):
    current = entry.get()
    if current == "Error":
        set_display(value)
    else:
        set_display(current + value)

def button_clear():
    set_display("")

def button_backspace_or_clear():
    current = entry.get()
    if ce_label_ref and ce_canvas_ref:
        label_text = ce_canvas_ref.itemcget(ce_label_ref, "text")
        if label_text == "AC":
            button_clear()
            ce_canvas_ref.itemconfig(ce_label_ref, text="CE")  # Reset to CE
        else:
            entry.config(state="normal")
            entry.delete(len(current)-1)
            entry.config(state="readonly")

def button_equal():
    try:
        expression = entry.get()
        expression = expression.replace("ln(", "math.log(")
        expression = expression.replace("log(", "math.log10(")
        expression = expression.replace("sin(", "math.sin(")
        expression = expression.replace("cos(", "math.cos(")
        expression = expression.replace("tan(", "math.tan(")
        expression = expression.replace("√(", "math.sqrt(")
        expression = expression.replace("π", str(math.pi))
        expression = expression.replace("e", str(math.e))
        expression = expression.replace("xʸ", "**")
        expression = expression.replace("%", "/100")
        expression = re.sub(r'(\d+)!', r'math.factorial(\1)', expression)
        expression = expression.replace("E", "*10**")

        result = eval(expression, {"math": math, "__builtins__": {}})
        set_display(str(result))

        if ce_label_ref and ce_canvas_ref:
            ce_canvas_ref.itemconfig(ce_label_ref, text="AC")
    except:
        set_display("Error")

buttons = [
    ("Rad", lambda: None), ("Deg", lambda: None), ("x!", lambda: button_click("!")), ("(", lambda: button_click("(")),
    (")", lambda: button_click(")")), ("%", lambda: button_click("%")), ("CE", lambda: button_backspace_or_clear()),
    ("Inv", lambda: None), ("sin", lambda: button_click("sin(")), ("ln", lambda: button_click("ln(")),
    ("7", lambda: button_click("7")), ("8", lambda: button_click("8")), ("9", lambda: button_click("9")), ("/", lambda: button_click("/")),
    ("π", lambda: button_click("π")), ("cos", lambda: button_click("cos(")), ("log", lambda: button_click("log(")),
    ("4", lambda: button_click("4")), ("5", lambda: button_click("5")), ("6", lambda: button_click("6")), ("*", lambda: button_click("*")),
    ("e", lambda: button_click("e")), ("tan", lambda: button_click("tan(")), ("√", lambda: button_click("√(")),
    ("1", lambda: button_click("1")), ("2", lambda: button_click("2")), ("3", lambda: button_click("3")), ("-", lambda: button_click("-")),
    ("Ans", lambda: None), ("EXP", lambda: button_click("E")), ("xʸ", lambda: button_click("**")),
    ("0", lambda: button_click("0")), (".", lambda: button_click(".")), ("=", button_equal), ("+", lambda: button_click("+"))
]

def create_pill_button(root, text, command, row, col, width=100, height=50, bg_color="#2b2f3a", hover_color="#3b3f4a"):
    canvas = tk.Canvas(root, width=width, height=height, bg="#1e1e1e", highlightthickness=0)
    canvas.grid(row=row, column=col, padx=5, pady=5)

    radius = height // 2
    pill = [
        canvas.create_oval(0, 0, height, height, fill=bg_color, outline=bg_color),
        canvas.create_oval(width - height, 0, width, height, fill=bg_color, outline=bg_color),
        canvas.create_rectangle(radius, 0, width - radius, height, fill=bg_color, outline=bg_color)
    ]
    label = canvas.create_text(width // 2, height // 2, text=text, fill="white", font=("Segoe UI", 10))

    def on_enter(e):
        for shape in pill:
            canvas.itemconfig(shape, fill=hover_color, outline=hover_color)

    def on_leave(e):
        for shape in pill:
            canvas.itemconfig(shape, fill=bg_color, outline=bg_color)

    def on_click(e):
        command()

    canvas.bind("<Enter>", on_enter)
    canvas.bind("<Leave>", on_leave)
    canvas.bind("<Button-1>", on_click)

    return canvas, label

highlight_buttons = {"1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."}
equal_button = "="

row_val = 1
col_val = 0
for (text, command) in buttons:
    if text in equal_button:
        color = "#adbfdc"
    elif text in highlight_buttons:
        color = "#5f6368"
    else:
        color = "#2c303d"
    hover_color = "#454a56" if text not in highlight_buttons else "#76797f"

    canvas, label = create_pill_button(root, text, command, row_val, col_val, bg_color=color, hover_color=hover_color)

    if text == "CE":
        ce_canvas_ref = canvas
        ce_label_ref = label

    col_val += 1
    if col_val > 6:
        col_val = 0
        row_val += 1

root.resizable(False, False)
root.mainloop()
