import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# Connect to database
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    roll TEXT PRIMARY KEY,
    name TEXT,
    marks TEXT
)
""")
conn.commit()

# Add Student
def add_student():
    roll = entry_roll.get()
    name = entry_name.get()
    marks = entry_marks.get()

    if roll == "" or name == "" or marks == "":
        messagebox.showwarning("Error", "All fields required!")
        return

    try:
        cursor.execute("INSERT INTO students VALUES (?, ?, ?)", (roll, name, marks))
        conn.commit()
        messagebox.showinfo("Success", "Student added!")
        clear_fields()
        view_students()
    except:
        messagebox.showerror("Error", "Roll number already exists!")

# View Students
def view_students():
    for row in tree.get_children():
        tree.delete(row)

    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", tk.END, values=row)

# Delete Student
def delete_student():
    roll = entry_roll.get()

    cursor.execute("DELETE FROM students WHERE roll=?", (roll,))
    conn.commit()

    messagebox.showinfo("Deleted", "Student removed!")
    view_students()
    clear_fields()

# Update Student
def update_student():
    roll = entry_roll.get()
    name = entry_name.get()
    marks = entry_marks.get()

    cursor.execute("UPDATE students SET name=?, marks=? WHERE roll=?", (name, marks, roll))
    conn.commit()

    messagebox.showinfo("Updated", "Student updated!")
    view_students()
    clear_fields()

# Clear Fields
def clear_fields():
    entry_roll.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_marks.delete(0, tk.END)

# GUI
root = tk.Tk()
root.title("Student Management System")
root.geometry("600x500")

tk.Label(root, text="Roll No").pack()
entry_roll = tk.Entry(root)
entry_roll.pack()

tk.Label(root, text="Name").pack()
entry_name = tk.Entry(root)
entry_name.pack()

tk.Label(root, text="Marks").pack()
entry_marks = tk.Entry(root)
entry_marks.pack()

tk.Button(root, text="Add", command=add_student).pack(pady=5)
tk.Button(root, text="Update", command=update_student).pack(pady=5)
tk.Button(root, text="Delete", command=delete_student).pack(pady=5)
tk.Button(root, text="View", command=view_students).pack(pady=5)

# Table
tree = ttk.Treeview(root, columns=("Roll", "Name", "Marks"), show="headings")
tree.heading("Roll", text="Roll")
tree.heading("Name", text="Name")
tree.heading("Marks", text="Marks")
tree.pack(fill=tk.BOTH, expand=True)

view_students()

root.mainloop()