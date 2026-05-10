import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

FILE_NAME = "contacts.json"


class ContactBookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book")
        self.root.geometry("950x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#f3f6fb")

        self.contacts = []
        self.filtered_contacts = []
        self.selected_index = None

        self.load_contacts()
        self.create_ui()
        self.refresh_list()

    def create_ui(self):
        # Title
        title_frame = tk.Frame(self.root, bg="#2563eb", height=70)
        title_frame.pack(fill="x")

        title_label = tk.Label(
            title_frame,
            text="Contact Book Application",
            bg="#2563eb",
            fg="white",
            font=("Arial", 20, "bold")
        )
        title_label.pack(pady=18)

        # Main frame
        main = tk.Frame(self.root, bg="#f3f6fb")
        main.pack(fill="both", expand=True, padx=15, pady=15)

        # Left panel - form
        left = tk.Frame(main, bg="white", bd=1, relief="solid")
        left.place(x=0, y=0, width=360, height=520)

        tk.Label(left, text="Contact Details", bg="white", fg="#111827",
                 font=("Arial", 16, "bold")).pack(anchor="w", padx=15, pady=(15, 10))

        self.name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.address_var = tk.StringVar()
        self.search_var = tk.StringVar()

        self.make_label_entry(left, "Name", self.name_var)
        self.make_label_entry(left, "Phone Number", self.phone_var)
        self.make_label_entry(left, "Email", self.email_var)
        self.make_label_entry(left, "Address", self.address_var)

        btn_frame = tk.Frame(left, bg="white")
        btn_frame.pack(fill="x", padx=15, pady=15)

        tk.Button(
            btn_frame, text="Add Contact", command=self.add_contact,
            bg="#16a34a", fg="white", font=("Arial", 11, "bold"),
            relief="flat", height=2
        ).pack(fill="x", pady=4)

        tk.Button(
            btn_frame, text="Update Contact", command=self.update_contact,
            bg="#f59e0b", fg="white", font=("Arial", 11, "bold"),
            relief="flat", height=2
        ).pack(fill="x", pady=4)

        tk.Button(
            btn_frame, text="Delete Contact", command=self.delete_contact,
            bg="#dc2626", fg="white", font=("Arial", 11, "bold"),
            relief="flat", height=2
        ).pack(fill="x", pady=4)

        tk.Button(
            btn_frame, text="Clear Fields", command=self.clear_fields,
            bg="#64748b", fg="white", font=("Arial", 11, "bold"),
            relief="flat", height=2
        ).pack(fill="x", pady=4)

        # Right panel - list and search
        right = tk.Frame(main, bg="white", bd=1, relief="solid")
        right.place(x=380, y=0, width=540, height=520)

        tk.Label(right, text="Saved Contacts", bg="white", fg="#111827",
                 font=("Arial", 16, "bold")).pack(anchor="w", padx=15, pady=(15, 8))

        search_frame = tk.Frame(right, bg="white")
        search_frame.pack(fill="x", padx=15, pady=(0, 10))

        tk.Label(search_frame, text="Search by name or phone", bg="white",
                 fg="#374151", font=("Arial", 10, "bold")).pack(anchor="w")

        search_entry = tk.Entry(search_frame, textvariable=self.search_var, font=("Arial", 11))
        search_entry.pack(fill="x", pady=5, ipady=6)
        search_entry.bind("<KeyRelease>", lambda e: self.search_contacts())

        list_frame = tk.Frame(right, bg="white")
        list_frame.pack(fill="both", expand=True, padx=15, pady=10)

        self.contact_listbox = tk.Listbox(
            list_frame,
            font=("Arial", 11),
            height=18,
            bg="#f8fafc",
            fg="#111827",
            selectbackground="#bfdbfe",
            selectforeground="#111827",
            relief="solid",
            bd=1
        )
        self.contact_listbox.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(list_frame, command=self.contact_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.contact_listbox.config(yscrollcommand=scrollbar.set)

        self.contact_listbox.bind("<<ListboxSelect>>", self.load_selected_contact)

        # Bottom status
        self.status_label = tk.Label(
            self.root,
            text="Ready",
            bg="#eaf1ff",
            fg="#1e3a8a",
            font=("Arial", 10, "bold"),
            anchor="w"
        )
        self.status_label.pack(fill="x", padx=15, pady=(0, 10))

    def make_label_entry(self, parent, label_text, text_var):
        frame = tk.Frame(parent, bg="white")
        frame.pack(fill="x", padx=15, pady=6)

        tk.Label(frame, text=label_text, bg="white", fg="#374151",
                 font=("Arial", 10, "bold")).pack(anchor="w")
        entry = tk.Entry(frame, textvariable=text_var, font=("Arial", 11))
        entry.pack(fill="x", pady=4, ipady=6)

    def add_contact(self):
        name = self.name_var.get().strip()
        phone = self.phone_var.get().strip()
        email = self.email_var.get().strip()
        address = self.address_var.get().strip()

        if not name or not phone:
            messagebox.showwarning("Warning", "Name and phone number are required.")
            return

        contact = {
            "name": name,
            "phone": phone,
            "email": email,
            "address": address
        }

        self.contacts.append(contact)
        self.save_contacts()
        self.refresh_list()
        self.clear_fields()
        self.status_label.config(text="Contact added successfully")

    def update_contact(self):
        if self.selected_index is None:
            messagebox.showwarning("Warning", "Please select a contact to update.")
            return

        selected_contact = self.filtered_contacts[self.selected_index]

        name = self.name_var.get().strip()
        phone = self.phone_var.get().strip()
        email = self.email_var.get().strip()
        address = self.address_var.get().strip()

        if not name or not phone:
            messagebox.showwarning("Warning", "Name and phone number are required.")
            return

        for i, contact in enumerate(self.contacts):
            if contact == selected_contact:
                self.contacts[i] = {
                    "name": name,
                    "phone": phone,
                    "email": email,
                    "address": address
                }
                break

        self.save_contacts()
        self.refresh_list()
        self.status_label.config(text="Contact updated successfully")

    def delete_contact(self):
        if self.selected_index is None:
            messagebox.showwarning("Warning", "Please select a contact to delete.")
            return

        selected_contact = self.filtered_contacts[self.selected_index]

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this contact?")
        if not confirm:
            return

        self.contacts = [c for c in self.contacts if c != selected_contact]
        self.save_contacts()
        self.refresh_list()
        self.clear_fields()
        self.status_label.config(text="Contact deleted successfully")

    def search_contacts(self):
        query = self.search_var.get().strip().lower()

        if query == "":
            self.filtered_contacts = self.contacts.copy()
        else:
            self.filtered_contacts = [
                contact for contact in self.contacts
                if query in contact["name"].lower() or query in contact["phone"].lower()
            ]

        self.populate_listbox()

    def refresh_list(self):
        self.filtered_contacts = self.contacts.copy()
        self.populate_listbox()

    def populate_listbox(self):
        self.contact_listbox.delete(0, tk.END)

        for contact in self.filtered_contacts:
            display_text = f"{contact['name']} - {contact['phone']}"
            self.contact_listbox.insert(tk.END, display_text)

        self.selected_index = None

    def load_selected_contact(self, event):
        selected = self.contact_listbox.curselection()
        if not selected:
            return

        index = selected[0]
        self.selected_index = index
        contact = self.filtered_contacts[index]

        self.name_var.set(contact["name"])
        self.phone_var.set(contact["phone"])
        self.email_var.set(contact["email"])
        self.address_var.set(contact["address"])

    def clear_fields(self):
        self.name_var.set("")
        self.phone_var.set("")
        self.email_var.set("")
        self.address_var.set("")
        self.contact_listbox.selection_clear(0, tk.END)
        self.selected_index = None
        self.status_label.config(text="Ready")

    def save_contacts(self):
        with open(FILE_NAME, "w", encoding="utf-8") as f:
            json.dump(self.contacts, f, indent=4)

    def load_contacts(self):
        if os.path.exists(FILE_NAME):
            try:
                with open(FILE_NAME, "r", encoding="utf-8") as f:
                    self.contacts = json.load(f)
            except Exception:
                self.contacts = []
        else:
            self.contacts = []


if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBookApp(root)
    root.mainloop()