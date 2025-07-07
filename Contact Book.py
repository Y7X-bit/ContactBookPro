import customtkinter as ctk
import csv
import os
from fpdf import FPDF
from tkinter import messagebox, filedialog

FILENAME = "contacts.csv"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class ContactBookApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("📇 Contact Book Pro – Symmetry Edition")
        self.geometry("720x800")
        self.configure(bg="#1c1c2e")
        self.resizable(False, False)

        # Title
        self.title_label = ctk.CTkLabel(
            self,
            text="📇 My Contact Book",
            font=("Segoe UI", 30, "bold"),
            text_color="#7FDBFF"
        )
        self.title_label.place(relx=0.5, y=30, anchor="n")

        # Form Frame
        self.form_card = ctk.CTkFrame(self, fg_color="#2b2b3d", corner_radius=25, width=660, height=230)
        self.form_card.place(x=30, y=100)

        entry_style = {
            "corner_radius": 20, "fg_color": "#38405F",
            "border_color": "#00BFFF", "text_color": "#ffffff"
        }
        self.entry_fname = ctk.CTkEntry(self.form_card, placeholder_text="First Name", width=300, **entry_style)
        self.entry_lname = ctk.CTkEntry(self.form_card, placeholder_text="Last Name", width=300, **entry_style)
        self.entry_email = ctk.CTkEntry(self.form_card, placeholder_text="Email", width=300, **entry_style)
        self.entry_phone = ctk.CTkEntry(self.form_card, placeholder_text="Phone", width=300, **entry_style)
        self.entry_address = ctk.CTkEntry(self.form_card, placeholder_text="Address", width=620, **entry_style)

        self.entry_fname.place(x=20, y=20)
        self.entry_lname.place(x=330, y=20)
        self.entry_email.place(x=20, y=75)
        self.entry_phone.place(x=330, y=75)
        self.entry_address.place(x=20, y=130)

        # Button Frame (Centered and Balanced)
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.place(relx=0.5, y=355, anchor="n")

        btn_style = {
            "corner_radius": 25, "height": 45, "width": 120,
            "font": ("Segoe UI", 13, "bold"),
            "fg_color": "#00BFFF", "hover_color": "#1E90FF", "text_color": "white"
        }

        buttons = [
            ("➕ Add", self.add_contact),
            ("✏️ Update", self.update_contact),
            ("❌ Delete", self.delete_contact),
            ("📄 PDF", self.export_pdf),
            ("🧹 Clear", self.clear_fields)
        ]

        for i, (text, command) in enumerate(buttons):
            left_pad = 18 if i == 0 else 8
            right_pad = 18 if i == len(buttons) - 1 else 8
            ctk.CTkButton(self.button_frame, text=text, command=command, **btn_style).pack(side="left", padx=(left_pad, right_pad))

        # Search Frame
        self.search_frame = ctk.CTkFrame(self, fg_color="#2A2E3F", corner_radius=20, width=660, height=260)
        self.search_frame.place(x=30, y=430)

        self.entry_search = ctk.CTkEntry(self.search_frame, placeholder_text="🔍 Search Name / Email / Phone",
                                         corner_radius=20, width=500,
                                         fg_color="#3a4458", border_color="#7FDBFF", text_color="#ffffff")
        self.entry_search.place(x=80, y=15)
        self.entry_search.bind("<KeyRelease>", self.search_contact)

        self.result_box = ctk.CTkTextbox(self.search_frame, height=180, width=620, corner_radius=20,
                                         font=("Consolas", 13), fg_color="#2E3548", text_color="#f0f0f0")
        self.result_box.place(x=20, y=55)

        # Load Contacts
        self.contacts = []
        self.load_contacts()
        self.show_contacts()

    def get_input_data(self):
        return [
            self.entry_fname.get().strip(),
            self.entry_lname.get().strip(),
            self.entry_email.get().strip(),
            self.entry_phone.get().strip(),
            self.entry_address.get().strip()
        ]

    def clear_fields(self):
        self.entry_fname.delete(0, ctk.END)
        self.entry_lname.delete(0, ctk.END)
        self.entry_email.delete(0, ctk.END)
        self.entry_phone.delete(0, ctk.END)
        self.entry_address.delete(0, ctk.END)
        self.entry_search.delete(0, ctk.END)
        self.result_box.delete("1.0", ctk.END)

    def load_contacts(self):
        if os.path.exists(FILENAME):
            with open(FILENAME, newline='') as file:
                reader = csv.reader(file)
                self.contacts = [row for row in reader if len(row) == 5]

    def save_contacts(self):
        with open(FILENAME, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(self.contacts)

    def add_contact(self):
        data = self.get_input_data()
        if not all(data):
            messagebox.showwarning("Warning", "Please fill all fields.")
            return
        self.contacts.append(data)
        self.save_contacts()
        self.clear_fields()
        self.show_contacts()

    def update_contact(self):
        search_term = self.entry_search.get().strip().lower()
        data = self.get_input_data()
        updated = False
        for i, contact in enumerate(self.contacts):
            if search_term in " ".join(contact).lower():
                self.contacts[i] = data
                updated = True
        if updated:
            self.save_contacts()
            messagebox.showinfo("Updated", "Contact updated successfully.")
            self.clear_fields()
            self.show_contacts()
        else:
            messagebox.showinfo("Not Found", "No matching contact found.")

    def delete_contact(self):
        search_term = self.entry_search.get().strip().lower()
        before = len(self.contacts)
        self.contacts = [c for c in self.contacts if search_term not in " ".join(c).lower()]
        if len(self.contacts) < before:
            self.save_contacts()
            messagebox.showinfo("Deleted", "Contact deleted.")
            self.clear_fields()
            self.show_contacts()
        else:
            messagebox.showinfo("Not Found", "No contact matched to delete.")

    def search_contact(self, event=None):
        search_term = self.entry_search.get().strip().lower()
        matches = [c for c in self.contacts if search_term in " ".join(c).lower()]
        self.show_contacts(matches)

    def show_contacts(self, contact_list=None):
        self.result_box.delete("1.0", ctk.END)
        for contact in contact_list or self.contacts:
            self.result_box.insert(ctk.END, f"Name: {contact[0]} {contact[1]}\n")
            self.result_box.insert(ctk.END, f"Email: {contact[2]}\nPhone: {contact[3]}\nAddress: {contact[4]}\n")
            self.result_box.insert(ctk.END, "-" * 60 + "\n")

    def export_pdf(self):
        if not self.contacts:
            messagebox.showinfo("Empty", "No contacts to export.")
            return

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        for contact in self.contacts:
            pdf.cell(200, 10, txt=f"Name: {contact[0]} {contact[1]}", ln=True)
            pdf.cell(200, 10, txt=f"Email: {contact[2]}", ln=True)
            pdf.cell(200, 10, txt=f"Phone: {contact[3]}", ln=True)
            pdf.cell(200, 10, txt=f"Address: {contact[4]}", ln=True)
            pdf.cell(200, 5, txt="-" * 100, ln=True)

        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            pdf.output(file_path)
            messagebox.showinfo("Success", "PDF exported!")


if __name__ == "__main__":
    app = ContactBookApp()
    app.mainloop()