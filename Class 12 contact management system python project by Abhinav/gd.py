
import customtkinter as ctk

import mysql.connector

from tkinter import messagebox

from tkinter import ttk

app = ctk.CTk()

app.geometry("600x400")

app.title("Contact Management System")

# Create a MySQL database connection

db_connection = mysql.connector.connect(

    host="localhost",

    user="root",

    password="12345",

    database="contactee"
)


# Create a cursor to execute SQL queries

db_cursor = db_connection.cursor()

#Defining font size

custom_font_size = 44


def main_screen():

    main_frame = ctk.CTkFrame(app)

    main_frame.pack(fill='both', expand=True)

    ctk.CTkLabel(main_frame, text="Contact Management System",font=(None,custom_font_size)).pack(pady=20)

    # Button to view contacts

    ctk.CTkButton(main_frame, text="View Contacts", command=view_contacts).pack(pady=10)

    # Button to add a new contact

    ctk.CTkButton(main_frame, text="Add Contact", command=add_contact).pack(pady=10)
    

#Viewing contacts window


def view_contacts():

    # Create a new top-level window for viewing contacts

    view_window = ctk.CTkToplevel(app)

    view_window.title("View Contacts")


    view_frame = ctk.CTkFrame(view_window)

    view_frame.pack(fill='both', expand=True)

    ctk.CTkLabel(view_frame, text="Contacts").pack(pady=20)


    # Create a Treeview widget for displaying contacts

    tree = ttk.Treeview(view_frame, columns=("ID", "Name", "Phone"), show="headings")


    # Define column headings

    tree.heading("ID", text="ID")

    tree.heading("Name", text="Name")

    tree.heading("Phone", text="Phone")


    # Set column widths

    tree.column("ID", width=300)

    tree.column("Name", width=450)

    tree.column("Phone", width=400)


    # Retrieve contacts from the database

    db_cursor.execute("SELECT id, name, phone FROM contacts")

    contacts = db_cursor.fetchall()


    # Insert the contacts into the Treeview

    for contact in contacts:

        tree.insert("", "end", values=contact)

    tree.pack(pady=10)


    #Button to view sorted contacts
    def view_sorted_contact():
        # Create a new top-level window for viewing contacts

        view_window = ctk.CTkToplevel(app)

        view_window.title("View Sorted Contacts")


        view_frame = ctk.CTkFrame(view_window)

        view_frame.pack(fill='both', expand=True)

        ctk.CTkLabel(view_frame, text="Contacts").pack(pady=20)


        # Create a Treeview widget for displaying contacts

        tree = ttk.Treeview(view_frame, columns=("ID", "Name", "Phone"), show="headings")


        # Define column headings

        tree.heading("ID", text="ID")

        tree.heading("Name", text="Name")

        tree.heading("Phone", text="Phone")


        # Set column widths

        tree.column("ID", width=300)

        tree.column("Name", width=450)
    
        tree.column("Phone", width=400)


        # Retrieve contacts from the database

        db_cursor.execute("SELECT id, name, phone FROM contacts ORDER BY id")

        contacts = db_cursor.fetchall()


        # Insert the contacts into the Treeview

        for contact in contacts:

            tree.insert("", "end", values=contact)
    
        tree.pack(pady=10)

        


    # Button to delete the selected contact


    def delete_selected_contact():

        selected_item = tree.selection()


        if not selected_item:

            messagebox.showerror("Error", "Please select a contact to delete.")

            return

        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this contact?")

        if confirm:

            contact_id = tree.item(selected_item, "values")[0]


            # Delete the contact from the database


            delete_query = "DELETE FROM contacts WHERE id = %s"

            db_cursor.execute(delete_query, (contact_id,))

            db_connection.commit()

            messagebox.showinfo("Success", "Contact deleted successfully!")


    # Refresh the contact list after deletion


            view_contacts()

    delete_button = ctk.CTkButton(view_frame, text="Delete Selected Contact", command=delete_selected_contact)

    delete_button.pack(pady=10)


    sort_button = ctk.CTkButton(view_frame, text="View Sorted Contact", command=view_sorted_contact)

    sort_button.pack(pady=10)


def add_contact():

    def save_contact():

        contact_id = id_entry.get()

        name = name_entry.get()

        phone = phone_entry.get()

        if contact_id and name and phone:

            # Insert the new contact into the database

            insert_query = "INSERT INTO contacts (id, name, phone) VALUES (%s, %s, %s)"

            values = (contact_id, name, phone)

            db_cursor.execute(insert_query, values)

            db_connection.commit()

            messagebox.showinfo("Success", "Contact added successfully!")

            add_window.destroy()

            view_contacts()

        else:

            messagebox.showerror("Error", "Please fill in all fields (ID, Name, and Phone).")


    add_window = ctk.CTkToplevel(app)

    add_window.title("Add New Contact")


    ctk.CTkLabel(add_window, text="Add New Contact").pack(pady=20)


    id_label = ctk.CTkLabel(add_window, text="ID")

    id_label.pack(pady=5)

    id_entry = ctk.CTkEntry(add_window, placeholder_text="Enter ID")

    id_entry.pack(pady=5)



    name_label = ctk.CTkLabel(add_window, text="Name")

    name_label.pack(pady=5)

    name_entry = ctk.CTkEntry(add_window, placeholder_text="Enter Name")

    name_entry.pack(pady=5)

    phone_label = ctk.CTkLabel(add_window, text="Phone")

    phone_label.pack(pady=5)

    phone_entry = ctk.CTkEntry(add_window, placeholder_text="Enter Phone")

    phone_entry.pack(pady=5)


    save_button = ctk.CTkButton(add_window, text="Save Contact", command=save_contact)

    save_button.pack(pady=10)


def delete_contact(contact_id):

    confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this contact?")

    if confirm:

        # Delete the contact from the database

        delete_query = "DELETE FROM contacts WHERE id = %s"

        db_cursor.execute(delete_query, (contact_id,))

        db_connection.commit()

        messagebox.showinfo("Success", "Contact deleted successfully!")

        view_contacts()


main_screen()

app.mainloop()
