import tkinter as tk
from tkinter import simpledialog
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image
import base64
import io
import imageio

def xor_encrypt_decrypt(data, key):
    from itertools import cycle
    # XOR шифрование/дешифрование данных
    return bytes(a ^ b for a, b in zip(data, cycle(key)))

def encode():
    key = simpledialog.askstring("Ключ", "Введите ключ шифрования:", show='*')
    if key is None: return  # Пользователь отменил ввод
    key = key.encode('utf-8')  # Преобразуем ключ в байты

    file_path = filedialog.askopenfilename()
    if file_path:
        extension = file_path.split('.')[-1]
        content_type = 'изображение' if extension in ['png', 'jpg', 'jpeg', 'gif'] else 'видео' if extension in ['mp4', 'avi', 'mov'] else 'аудио' if extension == 'mp3' else None
        if content_type is None:
            messagebox.showerror("Ошибка", "Формат файла не поддерживается!")
            return

        # Добавляем информацию о типе и формате файла в начало закодированного файла
        encoded_string = f"{content_type}:{extension}\n"

        if content_type == 'изображение':
            img = Image.open(file_path)
            buffered = io.BytesIO()
            img.save(buffered, format=extension.upper())
            encoded_bytes = base64.b64encode(xor_encrypt_decrypt(buffered.getvalue(), key))
            encoded_string += encoded_bytes.decode('utf-8')
        elif content_type == 'видео' or content_type == 'аудио':
            with open(file_path, "rb") as media_file:
                encoded_bytes = base64.b64encode(xor_encrypt_decrypt(media_file.read(), key))
                encoded_string += encoded_bytes.decode('utf-8')

        # Сохранение закодированного содержимого в текстовый файл
        text_file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        with open(text_file_path, "w") as text_file:
            text_file.write(encoded_string)
        messagebox.showinfo("Успех", "Файл успешно закодирован и сохранён!")

def decode():
    key = simpledialog.askstring("Ключ", "Введите ключ для дешифрования:", show='*')
    if key is None: return  # Пользователь отменил ввод
    key = key.encode('utf-8')  # Преобразуем ключ в байты

    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, "r") as text_file:
            content_info = text_file.readline().strip().split(':')
            content_type, extension = content_info
            encoded_string = text_file.read()

        decoded_bytes = xor_encrypt_decrypt(base64.b64decode(encoded_string), key)

        if content_type == 'изображение':
            img = Image.open(io.BytesIO(decoded_bytes))
            save_path = filedialog.asksaveasfilename(defaultextension=f".{extension}")
            img.save(save_path)
        elif content_type == 'видео' or content_type == 'аудио':
            save_path = filedialog.asksaveasfilename(defaultextension=f".{extension}")
            with open(save_path, "wb") as file_to_save:
                file_to_save.write(decoded_bytes)
        messagebox.showinfo("Успех", "Файл успешно декодирован и сохранён!")

# Создание графического интерфейса
root = tk.Tk()
root.title("Универсальный кодировщик и декодировщик с шифрованием")

encode_button = tk.Button(root, text="Кодировать", command=encode)
encode_button.pack(pady=5)

decode_button = tk.Button(root, text="Декодировать", command=decode)
decode_button.pack(pady=5)

root.mainloop()
