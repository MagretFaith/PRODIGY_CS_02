import os
from tkinter import Tk, Button, Label, Entry, filedialog, messagebox
from PIL import Image, ImageTk
import random


def initialize_random(key):
# Returns a random number generator initialized with a key (shift value).
    return random.Random(key)


def apply_shift_to_pixels(pixel_data, shift_value):
    # Shifts the pixel positions based on the provided shift_value.
    shifted_pixels = []
    for i in range(len(pixel_data)):
        shifted_pixels.append(pixel_data[(i + shift_value) % len(pixel_data)])
    return shifted_pixels


def scramble_image(input_path, output_path, password, shift_value):
    # Applies scrambling to the image's pixels based on the provided password and shift_value.
    img = Image.open(input_path)
    width, height = img.size
    pixel_data = list(img.getdata())
    rand_gen = initialize_random(password)

    indices = list(range(len(pixel_data)))
    rand_gen.shuffle(indices)
    scrambled_pixels = apply_shift_to_pixels([pixel_data[i] for i in indices], shift_value)

    scrambled_img = Image.new(img.mode, (width, height))
    scrambled_img.putdata(scrambled_pixels)
    scrambled_img.save(output_path)
    return scrambled_img


def restore_image(input_path, output_path, password, shift_value):
    # Restores the image by reversing the scrambling process using the password and shift_value.
    img = Image.open(input_path)
    width, height = img.size
    scrambled_pixels = list(img.getdata())
    rand_gen = initialize_random(password)

    # First reverse the shift applied during encryption
    shifted_pixels = apply_shift_to_pixels(scrambled_pixels, -shift_value)

    # Now restore the pixel order by reversing the shuffle using the same key
    indices = list(range(len(shifted_pixels)))
    rand_gen.shuffle(indices)

    # Reverse the shuffle order
    restored_pixels = [None] * len(shifted_pixels)
    for original_idx, shuffled_idx in enumerate(indices):
        restored_pixels[shuffled_idx] = shifted_pixels[original_idx]

    restored_img = Image.new(img.mode, (width, height))
    restored_img.putdata(restored_pixels)
    restored_img.save(output_path)
    return restored_img


def choose_input_image():
# Prompts the user to select an input image."""
    input_path = filedialog.askopenfilename(title="Choose Image")
    input_image_label.config(text=input_path)
    preview_image(input_path, input_image_preview)


def choose_output_image():
    # Prompts the user to choose a location to save the processed image."""
    output_path = filedialog.asksaveasfilename(defaultextension=".png",
                                               filetypes=[("PNG files", "*.png"),
                                                          ("JPEG files", "*.jpg;*.jpeg"),
                                                          ("All files", "*.*")],
                                               title="Save Processed Image")
    output_image_label.config(text=output_path)


def preview_image(image_path, label):
    # Displays a preview of the selected image."""
    img = Image.open(image_path)
    img.thumbnail((150, 150))
    img_display = ImageTk.PhotoImage(img)
    label.config(image=img_display)
    label.image = img_display


def encrypt_image():
    input_path = input_image_label.cget("text")
    output_path = output_image_label.cget("text")
    password = password_entry.get()
    shift_value = int(shift_entry.get())

    if not input_path or not output_path:
        messagebox.showerror("Error", "Please select input and output images.")
        return

    if not password:
        messagebox.showerror("Error", "Password is required for encryption.")
        return

    scrambled_img = scramble_image(input_path, output_path, password, shift_value)
    preview_image(output_path, encrypted_image_preview)
    messagebox.showinfo("Success", "Image has been Encrypted  successfully!")


def decrypt_image():
    input_path = input_image_label.cget("text")
    output_path = output_image_label.cget("text")
    password = password_entry.get()
    shift_value = int(shift_entry.get())

    if not input_path or not output_path:
        messagebox.showerror("Error", "Please select input and output images.")
        return

    if not password:
        messagebox.showerror("Error", "Password is required for decryption.")
        return

    restored_img = restore_image(input_path, output_path, password, shift_value)
    preview_image(output_path, decrypted_image_preview)
    messagebox.showinfo("Success", "Image has been Decrypted successfully!")


# Create the GUI window
root = Tk()
root.title("Image Encryption and Decryption  Tool")

# Create and place widgets
Label(root, text="Choose an image to Encrypt/Decrypt:").pack(pady=5)
input_image_label = Label(root, text="No image selected")
input_image_label.pack(pady=5)

Button(root, text="Browse", command=choose_input_image).pack(pady=5)

input_image_preview = Label(root)
input_image_preview.pack(pady=5)

Label(root, text="Select output image path:").pack(pady=5)
output_image_label = Label(root, text="No output path selected")
output_image_label.pack(pady=5)

Button(root, text="Save As", command=choose_output_image).pack(pady=5)

Label(root, text="Enter Encryption Password:").pack(pady=5)
password_entry = Entry(root, show="*")  # Password input (masked)
password_entry.pack(pady=5)

Label(root, text="Enter Shift Value (for pixel shifting):").pack(pady=5)
shift_entry = Entry(root)  # Shift value input
shift_entry.pack(pady=5)

Button(root, text="Encrypt Image", command=encrypt_image).pack(pady=5)
Button(root, text="Decrypt Image", command=decrypt_image).pack(pady=5)

# Output image preview for scrambled/restored image
encrypted_image_preview = Label(root)
encrypted_image_preview.pack(pady=5)

decrypted_image_preview = Label(root)
decrypted_image_preview.pack(pady=5)

# Start the GUI event loop
root.mainloop()

