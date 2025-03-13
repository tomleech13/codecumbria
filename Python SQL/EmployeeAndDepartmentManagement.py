import sqlite3
import matplotlib.pyplot as plt

# Connect to database
conn = sqlite3.connect("company.db")
cursor = conn.cursor()

# Create employees and departments tables if they don't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    department_id INTEGER,
    salary REAL,
    FOREIGN KEY (department_id) REFERENCES departments (id)
)
""")
conn.commit()

# Functions
def add_department():
    name = input("Enter department name: ")
    cursor.execute("INSERT INTO departments (name) VALUES (?)", (name,))
    conn.commit()
    print(f"\nDepartment {name} added successfully!\n")

def add_employee():
    name = input("Enter name: ")
    age = int(input("Enter age: "))
    department_id = int(input("Enter department ID: "))
    salary = float(input("Enter salary: "))

    cursor.execute("INSERT INTO employees (name, age, department_id, salary) VALUES (?, ?, ?, ?)",
                   (name, age, department_id, salary))
    conn.commit()
    print(f"\nEmployee {name} added successfully!\n")

def view_employees():
    cursor.execute("""
    SELECT employees.id, employees.name, employees.age, departments.name, employees.salary 
    FROM employees 
    JOIN departments ON employees.department_id = departments.id
    """)
    employees = cursor.fetchall()

    if not employees:
        print("\nNo employees found.\n")
    else:
        print("\nEmployee List:")
        for emp in employees:
            print(emp)
    print()

def update_employee_salary():
    emp_id = int(input("Enter Employee ID to update salary: "))

    cursor.execute("SELECT * FROM employees WHERE id = ?", (emp_id,))
    employee = cursor.fetchone()

    if not employee:
        print("\nEmployee not found!\n")
        return

    new_salary = float(input("Enter new salary: "))

    cursor.execute("UPDATE employees SET salary = ? WHERE id = ?", (new_salary, emp_id))
    conn.commit()
    print(f"\nEmployee ID {emp_id} salary updated successfully!\n")

def delete_employee():
    emp_id = int(input("Enter Employee ID to delete: "))

    cursor.execute("SELECT * FROM employees WHERE id = ?", (emp_id,))
    employee = cursor.fetchone()

    if not employee:
        print("\nEmployee not found!\n")
        return

    confirm = input(f"Are you sure you want to delete {employee[1]}? (yes/no): ").lower()
    if confirm == "yes":
        cursor.execute("DELETE FROM employees WHERE id = ?", (emp_id,))
        conn.commit()
        print(f"\nEmployee ID {emp_id} deleted successfully!\n")
    else:
        print("\nDelete action canceled.\n")

def department_employee_count():
    cursor.execute("""
    SELECT departments.name, COUNT(employees.id) 
    FROM employees 
    JOIN departments ON employees.department_id = departments.id 
    GROUP BY departments.name
    """)
    dept_counts = cursor.fetchall()

    if not dept_counts:
        print("\nNo departments or employees found.\n")
    else:
        print("\nDepartment-wise Employee Count:")
        for dept, count in dept_counts:
            print(f"{dept}: {count}")
        
        # Displaying the bar chart
        departments = [dept for dept, count in dept_counts]
        counts = [count for dept, count in dept_counts]
        plt.bar(departments, counts)
        plt.xlabel('Departments')
        plt.ylabel('Employee Count')
        plt.title('Employee Count by Department')
        plt.show()
    print()

# Menu function
def menu():
    while True:
        print("\nEmployee and Department Management System")
        print("1. Add Department")
        print("2. Add Employee")
        print("3. View Employees")
        print("4. Update Employee Salary")
        print("5. Delete Employee")
        print("6. Department-wise Employee Count")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_department()
        elif choice == "2":
            add_employee()
        elif choice == "3":
            view_employees()
        elif choice == "4":
            update_employee_salary()
        elif choice == "5":
            delete_employee()
        elif choice == "6":
            department_employee_count()
        elif choice == "7":
            print("\nExiting... Goodbye!")
            conn.close()
            break
        else:
            print("\nInvalid choice! Please enter a number between 1 and 7.\n")

# Run the menu
menu()