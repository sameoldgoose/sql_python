# a password manager application that securely stores and manages user passwords.
# type the name of the website and get the password for the website or save it
import sqlite3
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import messagebox

# Generate a key for encryption/decryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Connect to the SQLite database
conn = sqlite3.connect("passwords.db")
cursor = conn.cursor()

# Create the 'passwords' table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS passwords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        website TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
""")
conn.commit()

def encrypt_password(password):
    """Encrypt the given password using Fernet encryption."""
    return cipher_suite.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password):
    """Decrypt the given encrypted password using Fernet decryption."""
    return cipher_suite.decrypt(encrypted_password.encode()).decode()

def save_password():
    """Save the password in the 'passwords' table."""
    website = entry_website.get()
    username = entry_username.get()
    password = entry_password.get()

    if website and username and password:
        encrypted_password = encrypt_password(password)
        cursor.execute("""
            INSERT INTO passwords (website, username, password)
            VALUES (?, ?, ?)
        """, (website, username, encrypted_password))
        conn.commit()
        messagebox.showinfo("Success", "Password saved successfully.")
        entry_website.delete(0, tk.END)
        entry_username.delete(0, tk.END)
        entry_password.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Please fill in all the fields.")

def display_password():
    """Display the password for the given website from the 'passwords' table."""
    website = entry_website.get()

    if website:
        cursor.execute("""
            SELECT password FROM passwords WHERE website = ?
        """, (website,))
        row = cursor.fetchone()
        if row:
            encrypted_password = row[0]
            decrypted_password = decrypt_password(encrypted_password)
            messagebox.showinfo("Password", f"The password for {website} is: {decrypted_password}")
        else:
            messagebox.showinfo("Info", "No password found for the given website.")
        entry_website.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Please enter a website name.")

# Create the Tkinter application window
root = tk.Tk()
root.title("Password Manager")

# Create labels and entry fields
label_website = tk.Label(root, text="Website:")
entry_website = tk.Entry(root)
label_username = tk.Label(root, text="Username:")
entry_username = tk.Entry(root)
label_password = tk.Label(root, text="Password:")
entry_password = tk.Entry(root, show="*")
button_save = tk.Button(root, text="Save Password", command=save_password)
button_display = tk.Button(root, text="Display Password", command=display_password)

# Place the labels and entry fields in the grid
label_website.grid(row=0, column=0, padx=10, pady=10)
entry_website.grid(row=0, column=1, padx=10, pady=10)
label_username.grid(row=1, column=0, padx=10, pady=10)
entry_username.grid(row=1, column=1, padx=10, pady=10)
label_password.grid(row=2, column=0, padx=10, pady=10)
entry_password.grid(row=2, column=1, padx=10, pady=10)
button_save.grid(row=3, column=0, padx=10, pady=10)
button_display.grid(row=3, column=1, padx=10, pady=10)

# Start the Tkinter event loop
root.mainloop()
