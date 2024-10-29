import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

class UserManager:
    def __init__(self, filename='users.json'):
        self.filename = filename
        self.load_users()

    def load_users(self):
        """Load users from a JSON file."""
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                self.users = json.load(f)
        else:
            self.users = {}

    def save_users(self):
        """Save users to a JSON file."""
        with open(self.filename, 'w') as f:
            json.dump(self.users, f, indent=4)

    def register(self, username, password):
        """Register a new user."""
        if username in self.users:
            return False  # Username already exists
        self.users[username] = password
        self.save_users()
        return True

    def login(self, username, password):
        """Log in a user."""
        return self.users.get(username) == password

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login System")
        self.geometry("300x400")
        self.configure(bg='pink')  # Set the background color to pink
        self.user_manager = UserManager()
        self.create_styles()
        self.create_widgets()

    def create_styles(self):
        """Create custom styles for the application."""
        style = ttk.Style()
        style.configure('TFrame', background='pink')  # Set frame background to pink
        style.configure('TLabel', background='pink', foreground='black', font=('Arial', 12))  # Change foreground color to black
        style.configure('TButton', background='#5F9EA0', foreground='black', font=('Arial', 10, 'bold'))  # Button text color changed to black
        style.map('TButton', background=[('active', '#4B8B8B')])

    def create_widgets(self):
        # Create Login Frame
        self.login_frame = ttk.Frame(self)
        self.login_frame.pack(pady=20, padx=10, fill='both', expand=True)

        tk.Label(self.login_frame, text="Username").grid(row=0, column=0, pady=5)
        self.username_entry = ttk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1, pady=5)

        tk.Label(self.login_frame, text="Password").grid(row=1, column=0, pady=5)
        self.password_entry = ttk.Entry(self.login_frame, show='*')
        self.password_entry.grid(row=1, column=1, pady=5)

        tk.Button(self.login_frame, text="Login", command=self.login).grid(row=2, column=0, pady=10)
        tk.Button(self.login_frame, text="Register", command=self.show_registration).grid(row=2, column=1, pady=10)

    def show_registration(self):
        """Show registration form."""
        self.login_frame.pack_forget()
        self.registration_frame = ttk.Frame(self)
        self.registration_frame.pack(pady=20, padx=10, fill='both', expand=True)

        tk.Label(self.registration_frame, text="Username").grid(row=0, column=0, pady=5)
        self.reg_username_entry = ttk.Entry(self.registration_frame)
        self.reg_username_entry.grid(row=0, column=1, pady=5)

        tk.Label(self.registration_frame, text="Password").grid(row=1, column=0, pady=5)
        self.reg_password_entry = ttk.Entry(self.registration_frame, show='*')
        self.reg_password_entry.grid(row=1, column=1, pady=5)

        tk.Button(self.registration_frame, text="Register", command=self.register).grid(row=2, column=0, pady=10)
        tk.Button(self.registration_frame, text="Back to Login", command=self.show_login).grid(row=2, column=1, pady=10)

    def show_login(self):
        """Show login form."""
        self.registration_frame.pack_forget()
        self.login_frame.pack(pady=20, padx=10, fill='both', expand=True)

    def login(self):
        """Handle login logic."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check if fields are empty
        if not username or not password:
            messagebox.showwarning("Warning", "Both fields are required.")
            return

        if self.user_manager.login(username, password):
            messagebox.showinfo("Success", "Login Successful!")
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def register(self):
        """Handle registration logic."""
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()

        # Check if fields are empty
        if not username or not password:
            messagebox.showwarning("Warning", "Both fields are required.")
            return

        if self.user_manager.register(username, password):
            messagebox.showinfo("Success", "Registration Successful!")
            self.reg_username_entry.delete(0, tk.END)
            self.reg_password_entry.delete(0, tk.END)
            self.show_login()
        else:
            messagebox.showerror("Error", "Username already exists.")

if __name__ == "__main__":
    app = Application()
    app.mainloop()

