import database

selected_student = None  # Global variable

# Add student
def add(name_var, roll_var, marks_var):
    if name_var.get() == "" or roll_var.get() == "":
        return "Error: Name and Roll required"
    success = database.add_student(name_var.get(), roll_var.get(), marks_var.get())
    if success:
        return "Student Added!"
    else:
        return "Error: Roll number must be unique"

# Update student
def update(name_var, roll_var, marks_var):
    global selected_student
    if selected_student:
        database.update_student(selected_student[0], name_var.get(), roll_var.get(), marks_var.get())
        return "Student Updated!"
    else:
        return "Error: Select a student first"

# Delete student
def delete():
    global selected_student
    if selected_student:
        database.delete_student(selected_student[0])
        selected_student = None
        return "Student Deleted!"
    else:
        return "Error: Select a student first"

# Search student
def search(search_var):
    return database.search_students(search_var.get())

# View all
def view(order_by="id"):
    return database.get_students(order_by)
