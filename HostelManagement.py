import sqlite3
import streamlit as st

# Database functions
def create_connection():
    conn = sqlite3.connect('hostel_management.db')
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                        roll_no TEXT PRIMARY KEY,
                        name TEXT NOT NULL,
                        age INTEGER NOT NULL,
                        room_number TEXT NOT NULL
                      )''')
    conn.commit()
    conn.close()

def add_student(roll_no, name, age, room_number):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO students (roll_no, name, age, room_number) VALUES (?, ?, ?, ?)', (roll_no, name, age, room_number))
    conn.commit()
    conn.close()

def get_students():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students')
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_student(roll_no, name, age, room_number):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE students SET name = ?, age = ?, room_number = ? WHERE roll_no = ?', (name, age, room_number, roll_no))
    conn.commit()
    conn.close()

def delete_student(roll_no):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM students WHERE roll_no = ?', (roll_no,))
    conn.commit()
    conn.close()

# Initialize database
create_table()

# Streamlit App
def main():
    st.title("Hostel Management System")
    
    menu = ["Create", "Read", "Update", "Delete"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Create":
        st.subheader("Add Student")
        roll_no = st.text_input("Roll Number")
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=1)
        room_number = st.text_input("Room Number")
        
        if st.button("Add"):
            add_student(roll_no, name, age, room_number)
            st.success(f"Added {name} to the database")
    
    elif choice == "Read":
        st.subheader("View Students")
        students = get_students()
        
        for student in students:
            st.text(f"Roll Number: {student[0]}")
            st.text(f"Name: {student[1]}")
            st.text(f"Age: {student[2]}")
            st.text(f"Room Number: {student[3]}")
            st.text("---")
    
    elif choice == "Update":
        st.subheader("Update Student")
        students = get_students()
        student_dict = {student[0]: student for student in students}
        
        selected_roll_no = st.selectbox("Select Student by Roll Number", list(student_dict.keys()))
        selected_student = student_dict[selected_roll_no]
        
        name = st.text_input("Name", value=selected_student[1])
        age = st.number_input("Age", value=selected_student[2], min_value=1)
        room_number = st.text_input("Room Number", value=selected_student[3])
        
        if st.button("Update"):
            update_student(selected_roll_no, name, age, room_number)
            st.success(f"Updated student with Roll Number {selected_roll_no}")
    
    elif choice == "Delete":
        st.subheader("Delete Student")
        students = get_students()
        student_dict = {student[0]: student for student in students}
        
        selected_roll_no = st.selectbox("Select Student by Roll Number", list(student_dict.keys()))
        
        if st.button("Delete"):
            delete_student(selected_roll_no)
            st.success(f"Deleted student with Roll Number {selected_roll_no}")

if __name__ == '__main__':
    main()
