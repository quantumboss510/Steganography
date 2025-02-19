import cv2
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np


def encode_message(image_path, message, password, output_image):
    img = cv2.imread(image_path)
    if img is None:
        messagebox.showerror("Error", "Could not read the image.")
        return

    # Append a null terminator to signal end of message during decoding
    message += "\0"

    # Flatten the image to a 1D array
    flat = img.flatten()

    # Check if the message can fit in the image
    if len(message) > len(flat):
        messagebox.showerror("Error", "Message too long to encode in this image.")
        return

    # Encode the message by replacing pixel values with ASCII codes
    for i, char in enumerate(message):
        flat[i] = ord(char)

    # Reshape back to the original image dimensions and save
    encoded_img = flat.reshape(img.shape)
    cv2.imwrite(output_image, encoded_img)

    # Save the password in a file for decryption (in a real app, consider a more secure method)
    with open("password.txt", "w") as f:
        f.write(password)

    messagebox.showinfo("Success", f"Message encoded successfully in {output_image}")
    os.system(f"start {output_image}")  # Opens the image (Windows)


def browse_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    entry_image.delete(0, tk.END)
    entry_image.insert(0, file_path)


def encode():
    image_path = entry_image.get()
    message = entry_message.get()
    password = entry_password.get()
    output_image = "encryptedImage.png"

    if not image_path or not message or not password:
        messagebox.showerror("Error", "All fields are required!")
        return

    encode_message(image_path, message, password, output_image)


# GUI Setup
root = tk.Tk()
root.title("Image Steganography - Encoder")
root.geometry("400x300")

tk.Label(root, text="Select Image:").pack(pady=5)
entry_image = tk.Entry(root, width=40)
entry_image.pack(pady=5)
tk.Button(root, text="Browse", command=browse_image).pack(pady=5)

tk.Label(root, text="Enter Secret Message:").pack(pady=5)
entry_message = tk.Entry(root, width=40)
entry_message.pack(pady=5)

tk.Label(root, text="Set a Passcode:").pack(pady=5)
entry_password = tk.Entry(root, width=40, show="*")
entry_password.pack(pady=5)

tk.Button(root, text="Encode & Save", command=encode).pack(pady=10)

root.mainloop()
