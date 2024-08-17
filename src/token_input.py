import tkinter as tk
from tkinter import messagebox

def save_token():
    token = token_entry.get()
    if token:
        with open('token.txt', 'w') as file:
            file.write(token)
        messagebox.showinfo("Успех", "Токен сохранен!")
        root.destroy()  # Закрываем окно после сохранения токена
    else:
        messagebox.showerror("Ошибка", "Пожалуйста, введите токен!")

def bind_clipboard_shortcuts(entry):
    def copy(event=None):
        root.clipboard_clear()
        root.clipboard_append(entry.selection_get())

    def cut(event=None):
        copy()
        entry.delete("sel.first", "sel.last")

    def paste(event=None):
        entry.insert(tk.INSERT, root.clipboard_get())

    entry.bind("<Control-c>", copy)
    entry.bind("<Control-x>", cut)
    entry.bind("<Control-v>", paste)
    entry.bind("<Command-c>", copy)  # For macOS
    entry.bind("<Command-x>", cut)   # For macOS
    entry.bind("<Command-v>", paste) # For macOS

# Создаем главное окно
root = tk.Tk()
root.title("Введите ваш Telegram токен")

# Создаем метку и поле ввода
tk.Label(root, text="Telegram токен:").pack(pady=10)
token_entry = tk.Entry(root, width=50)
token_entry.pack(pady=5)

# Привязываем сочетания клавиш для копирования, вставки и вырезания
bind_clipboard_shortcuts(token_entry)

# Создаем кнопку для сохранения токена
tk.Button(root, text="Сохранить токен", command=save_token).pack(pady=20)

# Запуск основного цикла приложения
root.mainloop()
