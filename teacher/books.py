import tkinter as tk
import sqlite3

# Establish SQLite connection
conn = sqlite3.connect('bookstore.db')
cursor = conn.cursor()

# Create a table for books
cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        author TEXT,
        genre TEXT,
        price REAL,
        availability TEXT
    )
''')
conn.commit()

# Tkinter GUI setup
root = tk.Tk()
root.title("Online Bookstore")
root.configure(background="#F4F4F4")

# Create labels and entry fields
title_label = tk.Label(root, text="Title:", bg="#F4F4F4")
title_label.pack()
title_entry = tk.Entry(root)
title_entry.pack()

author_label = tk.Label(root, text="Author:", bg="#F4F4F4")
author_label.pack()
author_entry = tk.Entry(root)
author_entry.pack()

genre_label = tk.Label(root, text="Genre:", bg="#F4F4F4")
genre_label.pack()
genre_entry = tk.Entry(root)
genre_entry.pack()

price_label = tk.Label(root, text="Price:", bg="#F4F4F4")
price_label.pack()
price_entry = tk.Entry(root)
price_entry.pack()

availability_label = tk.Label(root, text="Availability:", bg="#F4F4F4")
availability_label.pack()

availability_frame = tk.Frame(root, bg="#F4F4F4")
availability_frame.pack()

availability_var = tk.StringVar(value="Yes")

availability_yes_radio = tk.Radiobutton(
    availability_frame,
    text="Yes",
    variable=availability_var,
    value="Yes",
    bg="#F4F4F4"
)
availability_yes_radio.pack(side=tk.LEFT)

availability_no_radio = tk.Radiobutton(
    availability_frame,
    text="No",
    variable=availability_var,
    value="No",
    bg="#F4F4F4"
)
availability_no_radio.pack(side=tk.LEFT)

book_listbox = tk.Listbox(root, width=50)
book_listbox.pack()

# Define bookstore functions
def add_book():
    title = title_entry.get()
    author = author_entry.get()
    genre = genre_entry.get()
    price = float(price_entry.get())
    availability = availability_var.get()

    cursor.execute('''
        INSERT INTO books (title, author, genre, price, availability)
        VALUES (?, ?, ?, ?, ?)
    ''', (title, author, genre, price, availability))
    conn.commit()
    display_books()

def display_books():
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()

    book_listbox.delete(0, tk.END)
    for book in books:
        book_listbox.insert(tk.END, f"{book[1]} by {book[2]} - {book[3]}")

def delete_book():
    selected_book = book_listbox.curselection()
    if selected_book:
        book_id = selected_book[0] + 1
        cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
        conn.commit()
        display_books()

def update_book():
    selected_book = book_listbox.curselection()
    if selected_book:
        book_id = selected_book[0] + 1
        title = title_entry.get()
        author = author_entry.get()
        genre = genre_entry.get()
        price = float(price_entry.get())
        availability = availability_var.get()

        cursor.execute('''
            UPDATE books SET title = ?, author = ?, genre = ?, price = ?, availability = ?
            WHERE id = ?
        ''', (title, author, genre, price, availability, book_id))
        conn.commit()
        display_books()

def clear_entries():
    title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    genre_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)
    availability_var.set("Yes")

# Create buttons
button_frame = tk.Frame(root, bg="#F4F4F4")
button_frame.pack()

add_button = tk.Button(button_frame, text="Add Book", command=add_book)
add_button.pack(side=tk.LEFT)

delete_button = tk.Button(button_frame, text="Delete Book", command=delete_book)
delete_button.pack(side=tk.LEFT)

update_button = tk.Button(button_frame, text="Update Book", command=update_book)
update_button.pack(side=tk.LEFT)

clear_button = tk.Button(button_frame, text="Clear Entries", command=clear_entries)
clear_button.pack(side=tk.LEFT)

# Display the books initially
display_books()

# Run the Tkinter main loop
root.mainloop()

# Close the SQLite connection
conn.close()
