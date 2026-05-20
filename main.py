from tkinter import *
from tkinter import ttk
import sqlite3

# ---------------- WINDOW ---------------- #

root = Tk()

root.title("Student Management System")
root.geometry("700x600")

# ---------------- DATABASE ---------------- #

conn = sqlite3.connect("students.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    roll TEXT,
    course TEXT,
    phone TEXT
)
""")

conn.commit()

# ---------------- FUNCTIONS ---------------- #

def show_students():

    # clear old data from table
    for data in student_table.get_children():
        student_table.delete(data)

    # fetch data from database
    cursor.execute("SELECT * FROM students")

    rows = cursor.fetchall()

    # insert data into table
    for row in rows:

        student_table.insert(
            parent='',
            index='end',
            iid=row[0],
            text='',
            values=row
        )

def add_student():

    name = name_entry.get()
    roll = roll_entry.get()
    course = course_entry.get()
    phone = phone_entry.get()

    # insert into database
    cursor.execute("""
    INSERT INTO students (name, roll, course, phone)
    VALUES (?, ?, ?, ?)
    """, (name, roll, course, phone))

    conn.commit()

    # refresh table
    show_students()

    # clear entry boxes
    name_entry.delete(0, END)
    roll_entry.delete(0, END)
    course_entry.delete(0, END)
    phone_entry.delete(0, END)
def delete_student():

    selected_item = student_table.selection()

    if selected_item:

        student_id = student_table.item(selected_item)['values'][0]

        cursor.execute(
            "DELETE FROM students WHERE id=?",
            (student_id,)
        )

        conn.commit()

        show_students()

        print("Student Deleted Successfully")

# ---------------- TITLE ---------------- #

title = Label(
    root,
    text="Student Management System",
    font=("Arial", 22, "bold")
)

title.pack(pady=20)

# ---------------- NAME ---------------- #

name_label = Label(root, text="Student Name")
name_label.pack()

name_entry = Entry(root, width=30)
name_entry.pack(pady=5)

# ---------------- ROLL ---------------- #

roll_label = Label(root, text="Roll Number")
roll_label.pack()

roll_entry = Entry(root, width=30)
roll_entry.pack(pady=5)

# ---------------- COURSE ---------------- #

course_label = Label(root, text="Course")
course_label.pack()

course_entry = Entry(root, width=30)
course_entry.pack(pady=5)

# ---------------- PHONE ---------------- #

phone_label = Label(root, text="Phone Number")
phone_label.pack()

phone_entry = Entry(root, width=30)
phone_entry.pack(pady=5)

# ---------------- BUTTON ---------------- #

add_btn = Button(
    root,
    text="Add Student",
    font=("Arial", 12, "bold"),
    bg="green",
    fg="white",
    command=add_student
)

add_btn.pack(pady=20)
delete_btn = Button(
    root,
    text="Delete Student",
    font=("Arial", 12, "bold"),
    bg="red",
    fg="white",
    command=delete_student
)

delete_btn.pack(pady=10)




# ---------------- TABLE ---------------- #

student_table = ttk.Treeview(root)

student_table['columns'] = ("ID", "Name", "Roll", "Course", "Phone")

# hide first empty column
student_table.column("#0", width=0, stretch=NO)

# columns
student_table.column("ID", anchor=CENTER, width=50)
student_table.column("Name", anchor=CENTER, width=150)
student_table.column("Roll", anchor=CENTER, width=100)
student_table.column("Course", anchor=CENTER, width=100)
student_table.column("Phone", anchor=CENTER, width=150)

# headings
student_table.heading("#0", text="", anchor=CENTER)

student_table.heading("ID", text="ID", anchor=CENTER)
student_table.heading("Name", text="Name", anchor=CENTER)
student_table.heading("Roll", text="Roll", anchor=CENTER)
student_table.heading("Course", text="Course", anchor=CENTER)
student_table.heading("Phone", text="Phone", anchor=CENTER)

student_table.pack(pady=20)

# ---------------- LOAD DATA ---------------- #

show_students()

# ---------------- MAINLOOP ---------------- #

root.mainloop()