import tkinter as tk
from tkinter import messagebox
import sqlite3

conn = sqlite3.connect('passwords.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS passwords
             (id INTEGER PRIMARY KEY, website TEXT, username TEXT, password TEXT)''')
conn.commit()

class PasswordManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager")
        self.root.geometry("400x300")

        self.website_label = tk.Label(root, text="Website:")
        self.website_label.grid(row=0, column=0, pady=5)
        self.website_entry = tk.Entry(root, width=30)
        self.website_entry.grid(row=0, column=1, pady=5)

        self.username_label = tk.Label(root, text="Username:")
        self.username_label.grid(row=1, column=0, pady=5)
        self.username_entry = tk.Entry(root, width=30)
        self.username_entry.grid(row=1, column=1, pady=5)

        self.password_label = tk.Label(root, text="Password:")
        self.password_label.grid(row=2, column=0, pady=5)
        self.password_entry = tk.Entry(root, width=30)
        self.password_entry.grid(row=2, column=1, pady=5)

        self.add_button = tk.Button(root, text="Add Password", command=self.add_password)
        self.add_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.view_button = tk.Button(root, text="View Passwords", command=self.view_passwords)
        self.view_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.password_list = tk.Listbox(root, width=50)
        self.password_list.grid(row=5, column=0, columnspan=2, pady=10)
        self.password_list.bind('<Double-1>', self.delete_password)

    def add_password(self):
        website = self.website_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        if website and username and password:
            c.execute("INSERT INTO passwords (website, username, password) VALUES (?, ?, ?)",
                      (website, username, password))
            conn.commit()
            messagebox.showinfo("Success", "Password added successfully!")
            self.website_entry.delete(0, tk.END)
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please fill out all fields.")

    def view_passwords(self):
        self.password_list.delete(0, tk.END)
        c.execute("SELECT * FROM passwords")
        for row in c.fetchall():
            self.password_list.insert(tk.END, f"Website: {row[1]}, Username: {row[2]}, Password: {row[3]}")

    def delete_password(self, event):
        selected_item = self.password_list.curselection()
        if selected_item:
            index = selected_item[0]
            item = self.password_list.get(index)
            website = item.split(', ')[0].split(': ')[1]
            username = item.split(', ')[1].split(': ')[1]
            c.execute("DELETE FROM passwords WHERE website = ? AND username = ?", (website, username))
            conn.commit()
            self.view_passwords()
            messagebox.showinfo("Success", "Password deleted successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManager(root)
    root.mainloop()
