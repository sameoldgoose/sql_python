import tkinter as tk
from tkinter import messagebox
import sqlite3

# Establish SQLite connection
conn = sqlite3.connect('recipes.db')
cursor = conn.cursor()

# Create a table for recipes
cursor.execute('''
    CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        ingredients TEXT,
        instructions TEXT
    )
''')
conn.commit()

# Tkinter GUI setup
root = tk.Tk()
root.title("Recipe Organizer")
root.configure(background="#F4F4F4")

# Create labels and entry fields for recipe information
# - Title
title_label = tk.Label(root, text="Title:", bg="#F4F4F4", font=("Arial", 14, "bold"))
title_label.pack()
title_entry = tk.Entry(root, font=("Arial", 12))
title_entry.pack()

# - Ingredients
ingredients_label = tk.Label(root, text="Ingredients:", bg="#F4F4F4", font=("Arial", 14, "bold"))
ingredients_label.pack()
ingredients_text = tk.Text(root, height=5, font=("Arial", 12))
ingredients_text.pack()

# - Instructions
instructions_label = tk.Label(root, text="Instructions:", bg="#F4F4F4", font=("Arial", 14, "bold"))
instructions_label.pack()
instructions_text = tk.Text(root, height=10, font=("Arial", 12))
instructions_text.pack()

# Listbox to display the recipes
recipe_listbox = tk.Listbox(root, width=50, font=("Arial", 12))
recipe_listbox.pack(pady=10)

# Define recipe organizer functions
# - Function to add a recipe
def add_recipe():
    """
    Add a recipe to the organizer database based on the provided information.
    """
    title = title_entry.get()
    ingredients = ingredients_text.get("1.0", tk.END)
    instructions = instructions_text.get("1.0", tk.END)

    cursor.execute('''
        INSERT INTO recipes (title, ingredients, instructions)
        VALUES (?, ?, ?)
    ''', (title, ingredients, instructions))
    conn.commit()
    display_recipes()

# - Function to display all recipes in the listbox
def display_recipes():
    """
    Retrieve all recipes from the organizer database and display them in the listbox.
    """
    cursor.execute('SELECT * FROM recipes')
    recipes = cursor.fetchall()

    recipe_listbox.delete(0, tk.END)
    for recipe in recipes:
        recipe_listbox.insert(tk.END, recipe[1])

# - Function to view the selected recipe
def view_recipe():
    """
    View the details of the selected recipe from the organizer database in a separate window.
    """
    selected_recipe = recipe_listbox.curselection()
    if selected_recipe:
        recipe_id = selected_recipe[0] + 1
        cursor.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,))
        recipe = cursor.fetchone()

        recipe_window = tk.Toplevel(root)
        recipe_window.title(recipe[1])
        recipe_window.configure(background="#F4F4F4")

        title_label = tk.Label(recipe_window, text=recipe[1], bg="#F4F4F4", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)

        ingredients_label = tk.Label(recipe_window, text="Ingredients:", bg="#F4F4F4", font=("Arial", 14, "bold"))
        ingredients_label.pack()
        ingredients_text = tk.Text(recipe_window, height=5, font=("Arial", 12))
        ingredients_text.insert(tk.END, recipe[2])
        ingredients_text.pack()

        instructions_label = tk.Label(recipe_window, text="Instructions:", bg="#F4F4F4", font=("Arial", 14, "bold"))
        instructions_label.pack()
        instructions_text = tk.Text(recipe_window, height=10, font=("Arial", 12))
        instructions_text.insert(tk.END, recipe[3])
        instructions_text.pack()

        recipe_window.mainloop()
    else:
        messagebox.showwarning("No Recipe Selected", "Please select a recipe to view.")

# - Function to delete the selected recipe
def delete_recipe():
    """
    Delete the selected recipe from the organizer database.
    """
    selected_recipe = recipe_listbox.curselection()
    if selected_recipe:
        recipe_id = selected_recipe[0] + 1
        cursor.execute('DELETE FROM recipes WHERE id = ?', (recipe_id,))
        conn.commit()
        display_recipes()
    else:
        messagebox.showwarning("No Recipe Selected", "Please select a recipe to delete.")

# Create buttons for adding and deleting recipes
button_frame = tk.Frame(root, bg="#F4F4F4")
button_frame.pack(pady=10)

add_button = tk.Button(button_frame, text="Add Recipe", command=add_recipe)
add_button.pack(side=tk.LEFT)

delete_button = tk.Button(button_frame, text="Delete Recipe", command=delete_recipe)
delete_button.pack(side=tk.LEFT)

# Display the recipes initially
display_recipes()

# Bind the view_recipe function to the listbox selection event
recipe_listbox.bind("<<ListboxSelect>>", lambda event: view_recipe())

# Run the Tkinter main loop
root.mainloop()

# Close the SQLite connection
conn.close()
