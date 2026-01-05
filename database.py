import sqlite3
from tkinter import *
from tkinter import messagebox

# --------------- Database Setup ---------------
conn = sqlite3.connect("students.db")
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    roll TEXT UNIQUE NOT NULL,
    marks INTEGER
)
""")
conn.commit()

# --------------- Functions ----------------
def add_student():
    if name_var.get() == "" or roll_var.get() == "":
        messagebox.showerror("Error", "Name and Roll No are required")
        return
    try:
        c.execute("INSERT INTO students (name, roll, marks) VALUES (?, ?, ?)",
                  (name_var.get(), roll_var.get(), marks_var.get()))
        conn.commit()
        messagebox.showinfo("Success", "Student Added!")
        clear_fields()
        view_students()
    except:
        messagebox.showerror("Error", "Roll number must be unique!")

def view_students():
    listbox.delete(0, END)
    c.execute("SELECT * FROM students")
    for row in c.fetchall():
        listbox.insert(END, row)

def select_student(event):
    global selected_student
    try:
        index = listbox.curselection()[0]
        selected_student = listbox.get(index)
        name_var.set(selected_student[1])
        roll_var.set(selected_student[2])
        marks_var.set(selected_student[3])
    except IndexError:
        pass

def update_student():
    if selected_student:
        c.execute("UPDATE students SET name=?, roll=?, marks=? WHERE id=?",
                  (name_var.get(), roll_var.get(), marks_var.get(), selected_student[0]))
        conn.commit()
        messagebox.showinfo("Success", "Student Updated!")
        clear_fields()
        view_students()

def delete_student():
    if selected_student:
        c.execute("DELETE FROM students WHERE id=?", (selected_student[0],))
        conn.commit()
        messagebox.showinfo("Success", "Student Deleted!")
        clear_fields()
        view_students()

def clear_fields():
    name_var.set("")
    roll_var.set("")
    marks_var.set("")

# --------------- GUI Setup ----------------
root = Tk()
root.title("Simple Student Management System")
root.geometry("500x350")

name_var = StringVar()
roll_var = StringVar()
marks_var = StringVar()
selected_student = None

# Labels & Entries
Label(root, text="Name").grid(row=0, column=0, padx=10, pady=5)
Entry(root, textvariable=name_var).grid(row=0, column=1)

Label(root, text="Roll No").grid(row=1, column=0, padx=10, pady=5)
Entry(root, textvariable=roll_var).grid(row=1, column=1)

Label(root, text="Marks").grid(row=2, column=0, padx=10, pady=5)
Entry(root, textvariable=marks_var).grid(row=2, column=1)

# Buttons
Button(root, text="Add", width=10, command=add_student).grid(row=3, column=0, pady=10)
Button(root, text="Update", width=10, command=update_student).grid(row=3, column=1)
Button(root, text="Delete", width=10, command=delete_student).grid(row=4, column=0)
Button(root, text="Clear", width=10, command=clear_fields).grid(row=4, column=1)

# Listbox
listbox = Listbox(root, width=50)
listbox.grid(row=0, column=2, rowspan=5, padx=10)
listbox.bind('<<ListboxSelect>>', select_student)

view_students()
root.mainloop()
