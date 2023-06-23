import tkinter as tk
import sqlite3

# Create a SQLite database connection

c = conn.cursor()

# Create a table to store student marks


# Function to insert student marks into the database
def insert_marks():
    
    conn.commit()
    clear_entries()
    display_marks()

# Function to display all student marks
def display_marks():
    

# Function to update student marks
def update_marks():
   
    conn.commit()
    clear_entries()
    display_marks()

# Function to delete student marks
def delete_marks():
    

    clear_entries()
    display_marks()

# Function to clear entry fields
def clear_entries():
   

# Create the GUI
root = tk.Tk()
root.title("Student Management App")

# Labels


# Entry fields

# Buttons


# Text display area


# Display initial marks

# Start the main loop
root.mainloop()

# Close the database connection
conn.close()
