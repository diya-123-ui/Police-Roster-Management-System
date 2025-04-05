#import necessary modules
import tkinter as tk
from tkinter import messagebox
import mysql.connector as ms
import random
#Establish connection
mycon = ms.connect(host="localhost", user="root", passwd='12345', database="police")
cursor = mycon.cursor()

def Register_Employee():
    print("\nEmployee Registration Menu~")
    
    # Generate a unique employee ID with a prefix "ER" followed by 4 random digits
    eid = "ER" + ''.join(random.choices('0123456789', k=4))
    ename = input("\tEnter Employee Name: ")
    area = input("\tEnter Assigned Location: ")
    dob = input("\tEnter DOB in the form YYYY-MM-DD: ")
    sex = input("\tEnter Gender of Employee: ")
    age = int(input("\tEnter Age of Employee: "))
    desig = input("\tEnter Designation of Employee: ")
    
    # Insert the entered details into the EMPLOYEE table and commit changes
    x = """insert into EMPLOYEE values('{0}', '{1}', '{2}',
        '{3}', '{4}', {5}, '{6}')""".format(eid, ename, area, dob, sex, age, desig)
    cursor.execute(x)
    mycon.commit()
    print("\nEmployee registered successfully!")

def Complaint_Register():
    print("Complaint Registration Menu~")
    loc = input("\tEnter location of Complaint Registration: ")
    desc = input("\tEnter your complaint: ")
    name = input("\tEnter your name: ")
    contact = input("\tEnter your contact details: ")
    # Generate a unique complaint ID using a random 2-digit number.
    c_id = "CM" + ''.join(random.choices('0123456789', k=2))
    query = "select EName from EMPLOYEE where Location='{}'".format(loc)
    cursor.execute(query)
    officer = cursor.fetchone()
    cursor.fetchall()
    if officer:
        officer_name = officer[0]
        print("Your complaint is registered. Officer {} will take charge.".format(officer_name))       
        x_query = """insert into USERCOMPLAINTS 
            (Location, Complaint_Description, Name_of_Complainant,Contact_Info,Complaint_ID) 
                values('{}','{}','{}','{}','{}')""".format(loc, desc, name, contact, c_id)
        cursor.execute(x_query)
        mycon.commit()
    else: # Notify the user if no officer is available for the entered location.
        print("No officers are available in your location. We will contact you shortly.")

def Roster_View():
    a = "police_UK@222" #Password for security purposes
    pwd = input("\nEnter Password To Access Roster Details:")
    if pwd==a:
        print("\nRoster View Menu~\n")
    
        query = "select * from EMPLOYEE"
        cursor.execute(query)
        employees = cursor.fetchall()
    
        # Print the column headers for better readability of the output
        print("{:<9}{:<8}{:<13}{:<8}{:<6}{:<10}".format
          ('ID', 'Name', 'Location', 'Gender', 'Age', 'Position'))
        print("-" * 65)
        for e in employees:
            print("{:<8}{:<9}{:<15}{:<6}{:<6}{:<10}".format
              (e[0], e[1], e[2], e[4], e[5], e[6]))
    else:
        print("\tWrong Password! Authorised Persons Only!")

def location():
    ea = input("\nEnter Location to Fetch Officers of that Area: ")
    q = "select EName from EMPLOYEE where Location='{}'".format(ea)
    # Execute the SQL query and fetch all matching records
    cursor.execute(q)
    record = cursor.fetchall()
    print("\nOfficers in ", ea)
    for z in record:
        print(z[0])

def eID():
    e = input("\nEnter ID to search: ")
    q = " select * from EMPLOYEE where EmpID='{}' ".format(e)
    cursor.execute(q)
    record = cursor.fetchone()
    # Display the employee's details if a matching record is retrieved.
    if record:
        print("\tEmployee Record Found:")
        print("\t\tEmpID:", record[0])
        print("\t\tName:", record[1])  
        print("\t\tDesignation:", record[6])  
    else:
        print("No employee found with that ID.")

def employee_status():
    ab = input("\nTo view 'Active Officers' (Type 1) or 'On Leave Officers' (Type 2): ")
    if ab == '1':
        print("\nActive Officers:")
        # Fetch & display all officers marked as 'Active' in the database.
        q1 = "select * from SHIFT_SALARY where Status='Active'"
        cursor.execute(q1)
        record = cursor.fetchall()
        for i in record:
            print(i[0])
    elif ab == "2":
        print("\nOfficers on Leave")
        # Fetch & display all officers marked as 'On Leave' in the database.
        q2 = "select * from SHIFT_SALARY where Status='On Leave'"
        cursor.execute(q2)
        record = cursor.fetchall()
        if record:
            for j in record:
                print(j[0])
        else:
            print("\nNo Officers on Leave")

def dep():
    dept = input("\nEnter Department to Retrieve Officers: ")

    # Query to fetch all employees of given designation from EMPLOYEE table.
    q = " select * from EMPLOYEE where Designation = '{}' ".format(dept)
    cursor.execute(q)
    record = cursor.fetchall()
    if record:
        print("\nList of ", dept, "Officers")
        for i in record:
            print(i[1])
    else:
        print("No Officers Designated as", dept)
        
def shift():
    print("\nDay Shift Officers~")
    q1 = "select * from SHIFT_SALARY where Shift_Type='Day'"
    cursor.execute(q1)
    record = cursor.fetchall() #Fetch Day shift officers
    for j in record:
        print(j[0])

    print("\nNight Shift Officers~")
    q2 = "select * from SHIFT_SALARY where Shift_Type='Night'"
    cursor.execute(q2)
    record = cursor.fetchall() #Fetch Night shift officers
    for x in record:
        print(x[0])

    print("\nEvening Shift Officers~")
    q3 = "select * from SHIFT_SALARY where Shift_Type='Evening'"
    cursor.execute(q3)
    record = cursor.fetchall() #Fetch Evening shift officers
    for y in record:
        print(y[0])

def allocate_leave():
    print("\nLeave Allocation window~")
    ename = input("\tEnter Employee Name: ")
    leave_type = input("\tEnter Leave Type (e.g., Sick, Vacation): ")
    start_date = input("\tEnter Leave Start Date (YYYY-MM-DD): ")
    end_date = input("\tEnter Leave End Date (YYYY-MM-DD): ")

    # Query to fetch the employee ID based on employee name.
    cursor.execute("""SELECT EmpID FROM employee
            WHERE EName = '{}'""".format(ename))
    res = cursor.fetchone()
    
    if res:
        emp_id = res[0]# Fetching employee ID from the result.
        
        cursor.execute("""INSERT INTO leaveassignment
            (EmpID, EName, Start_Date, End_Date, Leave_Type)
        VALUES (%s, %s, %s, %s, %s)""",(emp_id, ename, start_date,
                                        end_date, leave_type))
        mycon.commit()
        print("\tEmployee Leave Registered Succesfully!")
    else:
        print("Employee not found!")

def manage_salary():
    print("\nSalary Updation window~")
    emp_id = input("\tEnter Employee ID: ")
    salary = int(input("\tEnter Salary Amount (in $): "))
    cursor.execute("""update shift_salary set salary = {}
                   where empid ='{}'""".format
        (salary, emp_id))
    mycon.commit()
    print("\nSalary updated for Employee ID:",emp_id)

def assign_shift():
    print("\n\tShift Assignment window~")
    emp_id = input("Enter Employee ID: ")
    shift = input("Enter Shift (e.g., Day, Evening, Night): ")
    
    cursor.execute("""update shift_salary set Shift_Type='{}'
                where EmpID='{}'""".format(shift, emp_id))
    mycon.commit()
    print("\t",shift,"Shift assigned to Employee",emp_id)

def management_window():
    # Create a new window for Employee Management
    m_window = tk.Toplevel()
    m_window.title("Employee Management")
    m_window.geometry("400x300")
    
    # Define helper functions to call specific employee mng. operations
    def allocate_leave_b():   
        allocate_leave()

    def manage_salary_b():
        manage_salary()

    def assign_shift_b():
        assign_shift()
    # Add a title label at the top of the management window
    tk.Label(m_window, text="Employee Management Options",
             font=("Times New Roman", 16, "bold")).pack(pady=20)
    p = "lightblue"
    # Add buttons for each management functionality
    tk.Button(m_window, text="Allocate Leave", command=allocate_leave_b,
              width=30, bg=p).pack(pady=5)
    tk.Button(m_window, text="Manage Salaries", command=manage_salary_b,
              width=30, bg=p).pack(pady=5)
    tk.Button(m_window, text="Assign Shift", command=assign_shift_b,
              width=30, bg=p).pack(pady=5)

    # Start the main loop for this top-level window to keep it running independently
    m_window.mainloop()

def condition_window():
    c_window = tk.Toplevel()# Creating a new top-level window.
    c_window.title("Condition-Based Retrieval")
    c_window.geometry("400x300")

    # Nested functions to call specific management actions.
    def eID_b():
        eID()
    def dep_b():
        dep()
    def status_b():
        employee_status()
    def shift_b():
        shift()
    def location_b():
        location()

    # Adding a label to the management window.
    tk.Label(c_window,text="Select Condition",
             font=("Times New Roman", 16, "bold")).pack(pady=20)

    g = "lightgreen"
    # Adding buttons for each management action with corresponding commands.
    tk.Button(c_window,text="Search by Employee ID",command=eID_b,
              width=30, bg=g).pack(pady=5)
    tk.Button(c_window,text="Retrieve by Department",command=dep_b,
              width=30, bg=g).pack(pady=5)
    tk.Button(c_window,text="View Employee Status",command=status_b,
              width=30, bg=g).pack(pady=5)
    tk.Button(c_window,text="View by Shift Type",command=shift_b,
              width=30, bg=g).pack(pady=5)
    tk.Button(c_window,text="Retrieve by Location",command=location_b,
              width=30, bg=g).pack(pady=5)

    c_window.mainloop()# Starting the event loop for the management window.

def show_main_menu():
    # Create the main application window
    root = tk.Tk()
    root.title("Police Roster Management System")
    root.geometry("850x600")
    # Add a title label at the top of the main window
    tk.Label(root, text="POLICE ROSTER MANAGEMENT SYSTEM",
             font=("Times New Roman", 20,"bold"),fg="black").pack(pady=10)

    # Providing a descriptive text about the system and its purpose
    t = """POLICE DEPARTMENT - UNITED KINGDOM

This programme has been developed to manage and organize police rosters,
employee details, and public complaints.
Please use this system to avail other functionalities.

All complaints will be handled with due attention, and
the officers will be assigned to them accordingly.
This system is part of a wider effort to improve the functionality
of the police department in the digital era.
Thank you for choosing to use this system to ensure safer communities."""
    
    i_label = tk.Label(root,text=t,font=("Courier", 10),
                       fg="black",bg="white",justify="left",padx=10,pady=10)
    i_label.pack(pady=10)
    
    # Add a label to prompt the user to choose a functionality
    tk.Label(root, text="Choose any functionality", font=("Times New Roman", 13),
             fg="black").pack(pady=5)

    p = "lightpink"
    # Add buttons for different functionalities with respective command bindings
    tk.Button(root,text="Register Employee", command=Register_Employee,
              width=30, bg=p).pack(pady=5)
    tk.Button(root,text="Register Complaint", command=Complaint_Register,
              width=30, bg=p).pack(pady=5)
    tk.Button(root,text="Roster View", command=Roster_View,
              width=30, bg=p).pack(pady=5)
    tk.Button(root,text="Employee Management", command=management_window,
              width=30, bg=p).pack(pady=5)
    tk.Button(root,text="Condition-Based Retrieval", command=condition_window,
              width=30, bg=p).pack(pady=5)

    # Add an Exit button to close the application
    tk.Button(root,text="Exit", command=root.destroy,
              width=15, bg="lightyellow", fg="Black").pack(pady=20)

    # Run the main event loop for the application window
    root.mainloop()

# Call the main menu function to launch the application
show_main_menu()

# Close the MySQL connection when the program ends
mycon.close()
