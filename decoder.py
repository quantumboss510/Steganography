import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np


def decode_message(image_path, password):
   
    try:
        with open("password.txt", "r") as f:
            stored_password = f.read().strip()
    except FileNotFoundError:
        messagebox.showerror("Error", "No password file found.")
        return

    if password != stored_password:
        messagebox.showerror("Error", "Authentication Failed! Incorrect password.")
        return

    img = cv2.imread(image_path)
    if img is None:
        messagebox.showerror("Error", "Could not read the image.")
        return

   
    flat = img.flatten()

   
    message_chars = []
    for val in flat:
        char = chr(val)
        if char == "\0":
            break
        message_chars.append(char)
    message = "".join(message_chars)

    messagebox.showinfo("Decrypted Message", f"Message: {message}")


def browse_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    entry_image.delete(0, tk.END)
    entry_image.insert(0, file_path)


def decode():
    image_path = entry_image.get()
    password = entry_password.get()

    if not image_path or not password:
        messagebox.showerror("Error", "All fields are required!")
        return

    decode_message(image_path, password)



root = tk.Tk()
root.title("Image Steganography - Decoder")
root.geometry("400x250")

tk.Label(root, text="Select Encoded Image:").pack(pady=5)
entry_image = tk.Entry(root, width=40)
entry_image.pack(pady=5)
tk.Button(root, text="Browse", command=browse_image).pack(pady=5)

tk.Label(root, text="Enter Passcode:").pack(pady=5)
entry_password = tk.Entry(root, width=40, show="*")
entry_password.pack(pady=5)

tk.Button(root, text="Decode", command=decode).pack(pady=10)

root.mainloop()
