import tkinter as tk
import sqlite3

# Create a SQLite database connection
conn = sqlite3.connect('student.db')
c = conn.cursor()

# Create a table to store student marks
c.execute('''CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                science INTEGER,
                math INTEGER,
                english INTEGER
            )''')

# Function to insert student marks into the database
def insert_marks():
    name = entry_name.get()
    science = int(entry_science.get())
    math = int(entry_math.get())
    english = int(entry_english.get())
    
    c.execute("INSERT INTO students (name, science, math, english) VALUES (?, ?, ?, ?)",
              (name, science, math, english))
    
    conn.commit()
    clear_entries()
    display_marks()

# Function to display all student marks
def display_marks():
    c.execute("SELECT * FROM students")
    data = c.fetchall()
    
    # Clear the text widget
    text_display.delete(1.0, tk.END)
    
    for row in data:
        text_display.insert(tk.END, f"ID: {row[0]}\n")
        text_display.insert(tk.END, f"Name: {row[1]}\n")
        text_display.insert(tk.END, f"Science: {row[2]}\n")
        text_display.insert(tk.END, f"Math: {row[3]}\n")
        text_display.insert(tk.END, f"English: {row[4]}\n")
        text_display.insert(tk.END, "------------------------\n")

# Function to update student marks
def update_marks():
    selected_id = int(entry_id.get())
    name = entry_name.get()
    science = int(entry_science.get())
    math = int(entry_math.get())
    english = int(entry_english.get())
    
    c.execute("UPDATE students SET name=?, science=?, math=?, english=? WHERE id=?",
              (name, science, math, english, selected_id))
    
    conn.commit()
    clear_entries()
    display_marks()

# Function to delete student marks
def delete_marks():
    selected_id = int(entry_id.get())
    
    c.execute("DELETE FROM students WHERE id=?", (selected_id,))
    
    conn.commit()
    clear_entries()
    display_marks()

# Function to clear entry fields
def clear_entries():
    entry_id.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_science.delete(0, tk.END)
    entry_math.delete(0, tk.END)
    entry_english.delete(0, tk.END)

# Create the GUI
root = tk.Tk()
root.title("Student Management App")

# Labels
label_id = tk.Label(root, text="ID:")
label_id.grid(row=0, column=0, padx=10, pady=5)

label_name = tk.Label(root, text="Name:")
label_name.grid(row=1, column=0, padx=10, pady=5)

label_science = tk.Label(root, text="Science:")
label_science.grid(row=2, column=0, padx=10, pady=5)

label_math = tk.Label(root, text="Math:")
label_math.grid(row=3, column=0, padx=10, pady=5)

label_english = tk.Label(root, text="English:")
label_english.grid(row=4, column=0, padx=10, pady=5)

# Entry fields
entry_id = tk.Entry(root)
entry_id.grid(row=0, column=1, padx=10, pady=5)

entry_name = tk.Entry(root)
entry_name.grid(row=1, column=1, padx=10, pady=5)

entry_science = tk.Entry(root)
entry_science.grid(row=2, column=1, padx=10, pady=5)

entry_math = tk.Entry(root)
entry_math.grid(row=3, column=1, padx=10, pady=5)

entry_english = tk.Entry(root)
entry_english.grid(row=4, column=1, padx=10, pady=5)

# Buttons
button_insert = tk.Button(root, text="Insert Marks", command=insert_marks)
button_insert.grid(row=5, column=0, padx=10, pady=5)

button_update = tk.Button(root, text="Update Marks", command=update_marks)
button_update.grid(row=5, column=1, padx=10, pady=5)

button_delete = tk.Button(root, text="Delete Marks", command=delete_marks)
button_delete.grid(row=5, column=2, padx=10, pady=5)

# Text display area
text_display = tk.Text(root, width=40, height=10)
text_display.grid(row=6, column=0, columnspan=3, padx=10, pady=5)

# Display initial marks
display_marks()

# Start the main loop
root.mainloop()

# Close the database connection
conn.close()
