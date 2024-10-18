import mysql.connector
from tkinter import *
from tkinter import messagebox
import subprocess  # Import subprocess to call the home page

# Function to handle login
def login():
    username = login_username.get()
    password = login_password.get()

    if username == "" or password == "":
        messagebox.showerror("Error", "All fields are required")
        return

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="victory",  # MySQL password
            database="mydata"
        )
        cursor = conn.cursor()

        # Query to check if the user exists
        query = "SELECT * FROM users WHERE username=%s AND password=%s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()

        if result:
            messagebox.showinfo("Success", f"Login successful! Welcome {username}")
            conn.close()  # Close the database connection

            # Close the login window
            root.destroy()  # Close the current window

            # Open the home page
            subprocess.Popen(['python', 'home.py'])  # Call home.py
        else:
            messagebox.showerror("Error", "Login incorrect. Please try again.")

        conn.close()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

# Function to register a new user
def register_user():
    username = reg_username.get()
    password = reg_password.get()
    confirm_password = reg_confirm_password.get()
    role = reg_role.get()

    if username == "" or password == "" or confirm_password == "" or role == "":
        messagebox.showerror("Error", "All fields are required")
        return

    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match")
        return

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",  # MySQL username
            password="victory",  # MySQL password
            database="mydata"
        )
        cursor = conn.cursor()

        # Insert the new user into the database
        query = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, password, role))
        conn.commit()

        messagebox.showinfo("Success", "Registration successful")

        # Clear the fields
        reg_username_entry.delete(0, END)
        reg_password_entry.delete(0, END)
        reg_confirm_password_entry.delete(0, END)
        reg_role_entry.delete(0, END)

        conn.close()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

# Switch to registration page
def show_register_page():
    login_frame.pack_forget()
    register_frame.pack()

# Switch to login page
def show_login_page():
    register_frame.pack_forget()
    login_frame.pack()

# Create the main window
root = Tk()
root.title("Pharmacy Management System")
root.geometry("500x700")  # Adjusted window height
root.configure(bg="#B2E4B2")  # Set background color to pastel light green

# Login Frame
login_frame = Frame(root, bg="#B2E4B2")
login_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

Label(login_frame, text="Login", font=('Arial', 30), bg="#B2E4B2", fg="black").grid(row=0, column=0, columnspan=2, pady=(150, 10))  # Increased top padding

# Username and Password for Login
Label(login_frame, text="Username", bg="#B2E4B2", fg="black", font=('Arial', 16)).grid(row=1, column=0, padx=10, pady=(50, 5))
login_username = Entry(login_frame, font=('Arial', 16), width=20)
login_username.grid(row=1, column=1, padx=10, pady=(50, 5))

Label(login_frame, text="Password", bg="#B2E4B2", fg="black", font=('Arial', 16)).grid(row=2, column=0, padx=10, pady=(5, 5))  # Adjusted padding
login_password = Entry(login_frame, show="*", font=('Arial', 16), width=20)
login_password.grid(row=2, column=1, padx=10, pady=(5, 20))  # Reduced bottom padding


# Login Button
login_button = Button(login_frame, text="Login", command=login, font=('Arial', 16), width=10, bg="#FFB2D5")
login_button.grid(row=3, column=1, pady=10)

# Register redirect
Button(login_frame, text="Register", command=show_register_page, font=('Arial', 16), width=10, bg="#FF88C2").grid(row=4, column=1, pady=5)

# Registration Frame
register_frame = Frame(root, bg="#B2E4B2")

Label(register_frame, text="Register", font=('Arial', 30), bg="#B2E4B2", fg="black").grid(row=0, column=0, columnspan=2, pady=(150, 10))  # Increased top padding

# Username, Password, Confirm Password, and Role for Registration
Label(register_frame, text="Username", bg="#B2E4B2", fg="black", font=('Arial', 16)).grid(row=1, column=0, padx=10, pady=(50, 5))  # Increased padding
reg_username = StringVar()
reg_username_entry = Entry(register_frame, textvariable=reg_username, font=('Arial', 16), width=20)
reg_username_entry.grid(row=1, column=1, padx=10, pady=(50, 5))  # Increased padding

Label(register_frame, text="Password", bg="#B2E4B2", fg="black", font=('Arial', 16)).grid(row=2, column=0, padx=10, pady=(5, 5))  # Increased padding
reg_password = StringVar()
reg_password_entry = Entry(register_frame, textvariable=reg_password, show="*", font=('Arial', 16), width=20)
reg_password_entry.grid(row=2, column=1, padx=10, pady=(5, 5))  # Increased padding

Label(register_frame, text="Confirm Password", bg="#B2E4B2", fg="black", font=('Arial', 16)).grid(row=3, column=0, padx=10, pady=(5, 5))  # Increased padding
reg_confirm_password = StringVar()
reg_confirm_password_entry = Entry(register_frame, textvariable=reg_confirm_password, show="*", font=('Arial', 16), width=20)
reg_confirm_password_entry.grid(row=3, column=1, padx=10, pady=(5, 50))  # Increased padding

Label(register_frame, text="Role", bg="#B2E4B2", fg="black", font=('Arial', 16)).grid(row=4, column=0, padx=10, pady=(5, 5))  # Increased padding
reg_role = StringVar()
reg_role_entry = Entry(register_frame, textvariable=reg_role, font=('Arial', 16), width=20)
reg_role_entry.grid(row=4, column=1, padx=10, pady=(5, 50))  # Increased padding

# Register Button
register_button = Button(register_frame, text="Register", command=register_user, font=('Arial', 16), width=10, bg="#FF88C2")
register_button.grid(row=5, column=1, pady=10)

# Login redirect
Button(register_frame, text="Login", command=show_login_page, font=('Arial', 16), width=10, bg="#FFB2D5").grid(row=6, column=1, pady=5)

# Start with the login frame
show_login_page()
root.mainloop()