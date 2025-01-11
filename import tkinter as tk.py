import tkinter as tk
from tkinter import messagebox
import pyodbc

# Establish a connection to the SQL Server database
connection = pyodbc.connect('DRIVER={SQL Server};'
                            'SERVER=DESKTOP-SUV1PN2\SQLEXPRESS;'
                            'DATABASE=dhabank;'
                            'UID=dealga;'
                            'PWD=123;')

# Create a cursor object to execute SQL queries
cursor = connection.cursor()

def verify_password(account_num, password):
    try:
        # Execute SQL query to verify password
        cursor.execute(f"SELECT COUNT(*) FROM account WHERE account_num = ? AND password = ?", account_num, password)
        count = cursor.fetchone()[0]
        
        if count == 1:
            return True
        else:
            return False
    except Exception as e:
        messagebox.showerror("Error", f"Failed to verify password: {e}")
        return False


def deposit():
    account_num = account_num_entry.get()
    amount = amount_entry.get()
    password = password_entry.get()
    
    # Example: Get emp_id from a Tkinter Entry widget named emp_id_entry
    emp_id = emp_id_entry.get()

    try:
        # Verify password
        if verify_password(account_num, password):
            # Call deposit function with emp_id parameter
            deposit_transaction(emp_id, account_num, amount)
        else:
            messagebox.showerror("Error", "Incorrect password")
    except Exception as e:
        connection.rollback()
        messagebox.showerror("Error", f"Failed to deposit: {e}")

def deposit_transaction(emp_id, account_num, amount):
    try:
        # Execute SQL query to insert a new transaction for deposit
        cursor.execute("INSERT INTO transactions (emp_id, date, account_num, transaction_type, amount) VALUES (?, GETDATE(), ?, 'D', ?)", (emp_id, account_num, amount))
        connection.commit()

        messagebox.showinfo("Success", "Deposit successful")
    except Exception as e:
        connection.rollback()
        messagebox.showerror("Error", f"Failed to deposit: {e}")


# Function to handle withdrawal
def withdrawal():
    account_num = account_num_entry.get()
    amount = amount_entry.get()
    password = password_entry.get()
    
    # Example: Get emp_id from a Tkinter Entry widget named emp_id_entry
    emp_id = emp_id_entry.get()

    try:
        # Verify password
        if verify_password(account_num, password):
            # Call withdrawal function with emp_id parameter
            withdrawal_transaction(emp_id, account_num, amount)
        else:
            messagebox.showerror("Error", "Incorrect password")
    except Exception as e:
        connection.rollback()
        messagebox.showerror("Error", f"Failed to withdraw: {e}")

def withdrawal_transaction(emp_id, account_num, amount):
    try:
        # Execute SQL query to insert a new transaction for withdrawal
        cursor.execute("INSERT INTO transactions (emp_id, date, account_num, transaction_type, amount) VALUES (?, GETDATE(), ?, 'W', ?)", (emp_id, account_num, amount))
        connection.commit()

        messagebox.showinfo("Success", "Withdrawal successful")
    except Exception as e:
        connection.rollback()
        messagebox.showerror("Error", f"Failed to withdraw: {e}")



# Function to handle balance check
def check_balance():
    account_num = account_num_entry.get()
    password = password_entry.get()

    try:
        # Verify password
        if verify_password(account_num, password):
            # Execute SQL query to retrieve account balance
            cursor.execute(f"SELECT balance FROM account WHERE account_num = ?", account_num)
            row = cursor.fetchone()

            if row:
                balance = row.balance
                messagebox.showinfo("Balance", f"Account Balance: {balance}")
            else:
                messagebox.showerror("Error", "Account not found")
        else:
            messagebox.showerror("Error", "Incorrect password")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to check balance: {e}")
        
        
        
        
        
        
        
# Function to handle viewing transactions
def view_transactions():
    account_num = account_num_entry.get()

    try:
        # Execute SQL query to retrieve recent transactions
        cursor.execute("SELECT TOP 10 * FROM transactions WHERE account_num = ? ORDER BY date DESC", account_num)
        rows = cursor.fetchall()

        if rows:
            transaction_list = '\n'.join([f"Date: {row.date}, Type: {row.transaction_type}, Amount: {row.amount}" for row in rows])
            messagebox.showinfo("Recent Transactions", transaction_list)
        else:
            messagebox.showerror("Error", "No transactions found for this account")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to view transactions: {e}")


# Function to handle bank info search by IFSC
# Function to handle bank info search by IFSC
# Function to handle bank info search by IFSC
def search_by_ifsc():
    ifsccode = ifsc_entry.get().strip().upper()

    try:
        # Execute SQL query to retrieve bank information by IFSC
        cursor.execute(f"SELECT location FROM bank WHERE ifsccode = ?", ifsccode)
        row_bank = cursor.fetchone()

        if row_bank:
            location = row_bank.location
            
            # Retrieve employee details associated with the bank
            cursor.execute(f"SELECT emp_name, address, email FROM employee WHERE ifsccode = ?", ifsccode)
            row_employee = cursor.fetchone()

            if row_employee:
                emp_name = row_employee.emp_name
                address = row_employee.address
                email = row_employee.email

                messagebox.showinfo("Bank Information", f"IFSC: {ifsccode}\nLocation: {location}\n\nEmployee Details:\nName: {emp_name}\nAddress: {address}\nEmail: {email}")
            else:
                messagebox.showerror("Error", "Employee details not found for the provided IFSC code")
        else:
            messagebox.showerror("Error", "Bank not found for the provided IFSC code")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to retrieve bank information: {e}")
   



def get_account_information(emp_id, password):
    try:
        # Verify password for employee
        cursor.execute("SELECT COUNT(*) FROM employee WHERE emp_id = ? AND password = ?", emp_id, password)
        count = cursor.fetchone()[0]
        
        if count == 1:
            # Retrieve account information associated with the employee's bank
            cursor.execute("""
                SELECT a.account_num, a.balance
                FROM account a
                JOIN customer c ON a.cust_id = c.cust_id
                JOIN employee e ON c.ifsccode = e.ifsccode
                WHERE e.emp_id = ?
            """, emp_id)
            account_info = cursor.fetchall()

            if account_info:
                return account_info
            else:
                return None
        else:
            return None
    except Exception as e:
        messagebox.showerror("Error", f"Failed to retrieve account information: {e}")
        return None



def check_transactions():
    account_num = account_num_entry.get()
    password = password_entry.get()

    try:
        if verify_password(account_num, password):
            view_transactions()
        else:
            messagebox.showerror("Error", "Incorrect password")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to check transactions: {e}")

        
def employee_login():
    emp_id = emp_login_id_entry.get()
    password = emp_login_password_entry.get()
    
    # Get account information associated with the employee's bank
    account_info = get_account_information(emp_id, password)
    
    if account_info:
        # Display account information
        account_info_str = "\n".join([f"Account Number: {row.account_num}, Balance: {row.balance}" for row in account_info])
        messagebox.showinfo("Account Information", account_info_str)
    else:
        messagebox.showerror("Error", "Invalid Employee ID or Password")
        


# Create the main application window
app = tk.Tk()
app.title("Banking App")

# Create widgets for account number, amount, password, and buttons for various operations
account_num_label = tk.Label(app, text="Account Number:")
account_num_label.grid(row=0, column=0)
account_num_entry = tk.Entry(app)
account_num_entry.grid(row=0, column=1)

amount_label = tk.Label(app, text="Amount:")
amount_label.grid(row=1, column=0)
amount_entry = tk.Entry(app)
amount_entry.grid(row=1, column=1)

password_label = tk.Label(app, text="Password:")
password_label.grid(row=2, column=0)
password_entry = tk.Entry(app, show="*")
password_entry.grid(row=2, column=1)

# Create an Entry widget to get emp_id
emp_id_label = tk.Label(app, text="Employee ID:")
emp_id_label.grid(row=3, column=0)
emp_id_entry = tk.Entry(app)
emp_id_entry.grid(row=3, column=1)

deposit_button = tk.Button(app, text="Deposit", command=deposit)
deposit_button.grid(row=4, column=0)

withdrawal_button = tk.Button(app, text="Withdrawal", command=withdrawal)
withdrawal_button.grid(row=4, column=1)

balance_button = tk.Button(app, text="Check Balance", command=check_balance)
balance_button.grid(row=5, column=0)

# Widgets for searching bank info by IFSC
ifsc_label = tk.Label(app, text="IFSC Code:")
ifsc_label.grid(row=6, column=0)
ifsc_entry = tk.Entry(app)
ifsc_entry.grid(row=6, column=1)

search_button = tk.Button(app, text="Search by IFSC", command=search_by_ifsc)
search_button.grid(row=7, columnspan=2)

check_transactions_button = tk.Button(app, text="Check Transactions", command=check_transactions)
check_transactions_button.grid(row=8, columnspan=2)



# Create widgets for employee ID and password
emp_login_id_label = tk.Label(app, text="Employee ID:")
emp_login_id_label.grid(row=9, column=0)
emp_login_id_entry = tk.Entry(app)
emp_login_id_entry.grid(row=9, column=1)

emp_login_password_label = tk.Label(app, text="Employee Password:")
emp_login_password_label.grid(row=10, column=0)
emp_login_password_entry = tk.Entry(app, show="*")
emp_login_password_entry.grid(row=10, column=1)

# Button to trigger employee login and retrieve account information
emp_login_button = tk.Button(app, text="Employee Login and Get Account Info", command=employee_login)
emp_login_button.grid(row=11, columnspan=2)


app.mainloop()