import tkinter as tk
import sqlite3

# Establish SQLite connection
conn = sqlite3.connect("fitness_tracker.db")
cursor = conn.cursor()

# Create the "activities" table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS activities (
        id INTEGER PRIMARY KEY,
        activity_name TEXT,
        calories_burned INTEGER
    )
''')
conn.commit()

# Tkinter GUI setup
root = tk.Tk()
root.title("Fitness Tracker")

# Function to add an activity
def add_activity():
    activity_name = activity_entry.get()
    calories_burned = calories_entry.get()

    # Insert the activity into the database
    cursor.execute('INSERT INTO activities (activity_name, calories_burned) VALUES (?, ?)', (activity_name, calories_burned))
    conn.commit()

    # Clear the entry fields
    activity_entry.delete(0, tk.END)
    calories_entry.delete(0, tk.END)

    # Refresh the displayed activities and total calories
    display_activities()
    display_total_calories()

# Function to delete a selected activity
def delete_activity():
    # Get the selected activity
    selected_activity = activity_list.curselection()
    if selected_activity:
        activity_index = selected_activity[0]
        activity = activity_list.get(activity_index)

        # Extract the activity name from the list item
        activity_name = activity.split("-")[0].strip()

        # Delete the activity from the database
        cursor.execute('DELETE FROM activities WHERE activity_name = ?', (activity_name,))
        conn.commit()

        # Refresh the displayed activities and total calories
        display_activities()
        display_total_calories()

# Function to display the activities
def display_activities():
    # Clear the activity list
    activity_list.delete(0, tk.END)

    # Retrieve the activities from the database
    cursor.execute('SELECT * FROM activities')
    activities = cursor.fetchall()

    # Add each activity to the list
    for activity in activities:
        activity_list.insert(tk.END, f"{activity[1]} - Calories Burned: {activity[2]}")

# Function to display the total calories burned
def display_total_calories():
    # Retrieve the total calories burned from the database
    cursor.execute('SELECT SUM(calories_burned) FROM activities')
    total_calories = cursor.fetchone()[0]

    # Clear the total calories label
    total_calories_label.config(text="Total Calories Burned: ")

    # Display the total calories if available
    if total_calories is not None:
        total_calories_label.config(text=f"Total Calories Burned: {total_calories}")

# Labels and entry fields for activity information
activity_label = tk.Label(root, text="Activity:", font=("Arial", 12))
activity_label.pack()
activity_entry = tk.Entry(root, font=("Arial", 12))
activity_entry.pack()

calories_label = tk.Label(root, text="Calories Burned:", font=("Arial", 12))
calories_label.pack()
calories_entry = tk.Entry(root, font=("Arial", 12))
calories_entry.pack()

# Button to add an activity
add_button = tk.Button(root, text="Add Activity", command=add_activity, font=("Arial", 12))
add_button.pack(pady=10)

# Listbox to display the activities
activity_list = tk.Listbox(root, width=50, font=("Arial", 12))
activity_list.pack()

# Scrollbar for the activity list
scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
activity_list.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=activity_list.yview)

# Button to delete an activity
delete_button = tk.Button(root, text="Delete Activity", command=delete_activity, font=("Arial", 12))
delete_button.pack(pady=10)

# Label to display the total calories burned
total_calories_label = tk.Label(root, text="Total Calories Burned: ", font=("Arial", 12))
total_calories_label.pack()

# Run the Tkinter main loop
display_activities()
display_total_calories()

root.mainloop()

# Close the SQLite connection
conn.close()
