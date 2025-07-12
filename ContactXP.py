import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class ContactXP:
    def __init__(self, root):
        self.root = root
        self.root.title("ContactXP")  # Removed powered by Y7X here
        self.root.geometry("620x520")
        self.root.resizable(False, False)
        
        # Set Windows XP theme colors
        self.bg_color = "#ece9d8"
        self.button_color = "#d4d0c8"
        self.button_active = "#c0c0c0"
        self.highlight_color = "#316ac5"
        self.title_color = "#003399"
        self.text_color = "#000000"
        self.entry_bg = "#ffffff"
        self.entry_select = "#f5d9a6"
        
        # Initialize contacts list
        self.contacts = []
        
        # Create UI first
        self.create_title_bar()
        self.create_widgets()
        
        # Then load contacts (which will use the now-created UI elements)
        self.load_contacts()
        
    def create_title_bar(self):
        # XP-style gradient title bar
        title_frame = tk.Frame(self.root, bg=self.title_color, height=25, bd=0)
        title_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            title_frame,
            text="ContactXP",
            font=("Tahoma", 10, "bold"),
            fg="white",
            bg=self.title_color,
            padx=10
        )
        title_label.pack(side=tk.LEFT)
        
        # Minimize button
        min_btn = tk.Label(
            title_frame,
            text="_",
            font=("Tahoma", 12, "bold"),
            fg="white",
            bg=self.title_color,
            padx=8
        )
        min_btn.pack(side=tk.RIGHT)
        min_btn.bind("<Button-1>", lambda e: self.root.state('iconic'))
        
        # Close button
        close_btn = tk.Label(
            title_frame,
            text="×",
            font=("Tahoma", 12, "bold"),
            fg="white",
            bg=self.title_color,
            padx=8
        )
        close_btn.pack(side=tk.RIGHT)
        close_btn.bind("<Button-1>", lambda e: self.root.destroy())
        
    def create_widgets(self):
        # Main frame with XP-style border
        main_frame = tk.Frame(
            self.root,
            bg=self.bg_color,
            bd=1,
            relief=tk.SUNKEN
        )
        main_frame.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        
        # Toolbar with XP-style gradient
        toolbar = tk.Frame(
            main_frame,
            bg=self.bg_color,
            height=30,
            bd=1,
            relief=tk.RAISED
        )
        toolbar.pack(fill=tk.X, padx=2, pady=2)
        
        # Toolbar buttons
        btn_style = {
            "font": ("Tahoma", 8),
            "fg": self.text_color,
            "bg": self.button_color,
            "activeforeground": self.text_color,
            "activebackground": self.button_active,
            "relief": tk.RAISED,
            "bd": 1,
            "padx": 6,
            "pady": 1
        }
        
        add_btn = tk.Button(
            toolbar,
            text="Add",
            command=self.add_contact_window,
            **btn_style
        )
        add_btn.pack(side=tk.LEFT, padx=2)
        
        edit_btn = tk.Button(
            toolbar,
            text="Edit",
            command=self.edit_contact,
            **btn_style
        )
        edit_btn.pack(side=tk.LEFT, padx=2)
        
        delete_btn = tk.Button(
            toolbar,
            text="Delete",
            command=self.delete_contact,
            **btn_style
        )
        delete_btn.pack(side=tk.LEFT, padx=2)
        
        # Search frame
        search_frame = tk.Frame(main_frame, bg=self.bg_color)
        search_frame.pack(fill=tk.X, pady=4, padx=4)
        
        tk.Label(
            search_frame,
            text="Search:",
            font=("Tahoma", 9),
            fg=self.text_color,
            bg=self.bg_color
        ).pack(side=tk.LEFT)
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=("Tahoma", 9),
            fg=self.text_color,
            bg=self.entry_bg,
            relief=tk.SUNKEN,
            bd=1,
            selectbackground=self.entry_select,
            width=30
        )
        search_entry.pack(side=tk.LEFT, padx=4, ipady=2)
        search_entry.bind("<KeyRelease>", self.search_contacts)
        
        search_btn = tk.Button(
            search_frame,
            text="Search",
            command=self.search_contacts,
            **btn_style
        )
        search_btn.pack(side=tk.LEFT)
        
        # Contact list with XP-style scrollbar
        list_frame = tk.Frame(main_frame, bg=self.bg_color)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        
        self.tree = ttk.Treeview(
            list_frame,
            columns=("Name", "Phone", "Email"),
            show="headings",
            selectmode="browse",
            height=15
        )
        
        # Style the treeview to match Windows XP
        style = ttk.Style()
        style.theme_use("default")
        
        style.configure(
            "Treeview",
            background=self.entry_bg,
            foreground=self.text_color,
            fieldbackground=self.entry_bg,
            bordercolor=self.bg_color,
            borderwidth=0,
            font=("Tahoma", 9),
            rowheight=20
        )
        
        style.configure(
            "Treeview.Heading",
            background=self.button_color,
            foreground=self.text_color,
            relief=tk.RAISED,
            font=("Tahoma", 9, "bold"),
            padding=(0, 3, 0, 3)
        )
        
        style.map(
            "Treeview",
            background=[("selected", self.highlight_color)],
            foreground=[("selected", "white")]
        )
        
        # Configure XP-style scrollbar
        style.configure(
            "Vertical.TScrollbar",
            arrowsize=15,
            gripcount=0,
            background=self.button_color,
            troughcolor=self.bg_color,
            bordercolor=self.bg_color,
            arrowcolor=self.text_color,
            relief=tk.RAISED
        )
        
        self.tree.heading("Name", text="Name")
        self.tree.heading("Phone", text="Phone")
        self.tree.heading("Email", text="Email")
        
        self.tree.column("Name", width=180, anchor=tk.W)
        self.tree.column("Phone", width=120, anchor=tk.W)
        self.tree.column("Email", width=200, anchor=tk.W)
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_bar = tk.Frame(
            main_frame,
            bg=self.bg_color,
            height=20,
            bd=1,
            relief=tk.SUNKEN
        )
        self.status_bar.pack(fill=tk.X, padx=2, pady=2)
        
        self.status_label = tk.Label(
            self.status_bar,
            text="Ready",
            font=("Tahoma", 8),
            fg=self.text_color,
            bg=self.bg_color,
            anchor=tk.W
        )
        self.status_label.pack(fill=tk.X, padx=4)
        
        # Branding label at the bottom
        self.branding_label = tk.Label(
            main_frame,
            text="🔎 Powered by Y7X 💗",
            font=("Tahoma", 8, "italic"),
            fg=self.title_color,
            bg=self.bg_color,
            anchor=tk.E
        )
        self.branding_label.pack(fill=tk.X, padx=4, pady=(0,4))
    
    def update_status(self, message):
        self.status_label.config(text=message)
    
    def load_contacts(self):
        if os.path.exists("contacts.json"):
            try:
                with open("contacts.json", "r") as f:
                    self.contacts = json.load(f)
                self.update_status("Contacts loaded successfully")
            except:
                self.contacts = []
                self.update_status("Error loading contacts - created new file")
        else:
            self.contacts = []
            self.update_status("No contacts file found - created new one")
        self.update_contact_list()
    
    def save_contacts(self):
        with open("contacts.json", "w") as f:
            json.dump(self.contacts, f)
        self.update_status("Contacts saved successfully")
    
    def update_contact_list(self, contacts=None):
        self.tree.delete(*self.tree.get_children())
        contacts = contacts or self.contacts
        for contact in contacts:
            self.tree.insert("", tk.END, values=(contact["name"], contact["phone"], contact["email"]))
        self.update_status(f"Showing {len(contacts)} contacts")
    
    def search_contacts(self, event=None):
        query = self.search_var.get().lower()
        if not query:
            self.update_contact_list()
            self.update_status("Search cleared")
            return
        
        results = [
            contact for contact in self.contacts
            if (query in contact["name"].lower() or 
                query in contact["phone"].lower() or 
                query in contact["email"].lower())
        ]
        self.update_contact_list(results)
        self.update_status(f"Found {len(results)} matching contacts")
    
    def add_contact_window(self):
        self.contact_form("Add New Contact", self.save_new_contact)
    
    def edit_contact(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a contact to edit", parent=self.root)
            return
        
        item = self.tree.item(selected[0])
        contact = {
            "name": item["values"][0],
            "phone": item["values"][1],
            "email": item["values"][2]
        }
        self.contact_form("Edit Contact", self.update_contact, contact)
    
    def contact_form(self, title, submit_action, contact=None):
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry("380x220")
        window.configure(bg=self.bg_color)
        window.resizable(False, False)
        
        # XP-style form border
        form_border = tk.Frame(window, bg=self.bg_color, bd=1, relief=tk.SUNKEN)
        form_border.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        
        # Form frame
        form_frame = tk.Frame(form_border, bg=self.bg_color)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        
        # Form labels
        tk.Label(
            form_frame,
            text="Name:",
            font=("Tahoma", 9),
            fg=self.text_color,
            bg=self.bg_color
        ).grid(row=0, column=0, sticky="w", pady=4)
        
        tk.Label(
            form_frame,
            text="Phone:",
            font=("Tahoma", 9),
            fg=self.text_color,
            bg=self.bg_color
        ).grid(row=1, column=0, sticky="w", pady=4)
        
        tk.Label(
            form_frame,
            text="Email:",
            font=("Tahoma", 9),
            fg=self.text_color,
            bg=self.bg_color
        ).grid(row=2, column=0, sticky="w", pady=4)
        
        # Form entries
        name_var = tk.StringVar(value=contact["name"] if contact else "")
        phone_var = tk.StringVar(value=contact["phone"] if contact else "")
        email_var = tk.StringVar(value=contact["email"] if contact else "")
        
        entry_style = {
            "font": ("Tahoma", 9),
            "fg": self.text_color,
            "bg": self.entry_bg,
            "relief": tk.SUNKEN,
            "bd": 1,
            "selectbackground": self.entry_select,
            "width": 30
        }
        
        name_entry = tk.Entry(form_frame, textvariable=name_var, **entry_style)
        name_entry.grid(row=0, column=1, sticky="ew", padx=4, pady=4, ipady=2)
        
        phone_entry = tk.Entry(form_frame, textvariable=phone_var, **entry_style)
        phone_entry.grid(row=1, column=1, sticky="ew", padx=4, pady=4, ipady=2)
        
        email_entry = tk.Entry(form_frame, textvariable=email_var, **entry_style)
        email_entry.grid(row=2, column=1, sticky="ew", padx=4, pady=4, ipady=2)
        
        # Button frame
        btn_frame = tk.Frame(form_frame, bg=self.bg_color)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=8)
        
        # XP-style form buttons
        form_btn_style = {
            "font": ("Tahoma", 9),
            "fg": self.text_color,
            "bg": self.button_color,
            "activeforeground": self.text_color,
            "activebackground": self.button_active,
            "relief": tk.RAISED,
            "bd": 1,
            "padx": 8,
            "pady": 1
        }
        
        submit_btn = tk.Button(
            btn_frame,
            text="Save" if contact else "Add",
            command=lambda: submit_action(name_var.get(), phone_var.get(), email_var.get(), window),
            **form_btn_style
        )
        submit_btn.pack(side=tk.LEFT, padx=4)
        
        cancel_btn = tk.Button(
            btn_frame,
            text="Cancel",
            command=window.destroy,
            **form_btn_style
        )
        cancel_btn.pack(side=tk.LEFT, padx=4)
        
        # Make form responsive
        form_frame.columnconfigure(1, weight=1)
        name_entry.focus()
    
    def save_new_contact(self, name, phone, email, window):
        if not name or not phone:
            messagebox.showwarning("Warning", "Name and Phone are required fields", parent=window)
            return
        
        self.contacts.append({
            "name": name,
            "phone": phone,
            "email": email
        })
        self.save_contacts()
        self.update_contact_list()
        window.destroy()
        self.update_status("Contact added successfully")
    
    def update_contact(self, name, phone, email, window):
        if not name or not phone:
            messagebox.showwarning("Warning", "Name and Phone are required fields", parent=window)
            return
        
        selected = self.tree.selection()[0]
        index = self.tree.index(selected)
        
        self.contacts[index] = {
            "name": name,
            "phone": phone,
            "email": email
        }
        self.save_contacts()
        self.update_contact_list()
        window.destroy()
        self.update_status("Contact updated successfully")
    
    def delete_contact(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a contact to delete", parent=self.root)
            return
        
        if messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this contact?",
            icon="warning",
            parent=self.root
        ):
            index = self.tree.index(selected[0])
            del self.contacts[index]
            self.save_contacts()
            self.update_contact_list()
            self.update_status("Contact deleted successfully")

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactXP(root)
    root.mainloop()