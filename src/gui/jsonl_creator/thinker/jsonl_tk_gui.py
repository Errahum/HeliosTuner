import tkinter as tk
from tkinter import messagebox
from src.utils.jsonl_creator.jsonl_creator import create_jsonl_entry, save_to_jsonl


class JsonlCreatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("JSONL Creator")
        self.geometry("500x400")

        # System Role
        self.system_label = tk.Label(self, text="System Role")
        self.system_label.pack()
        self.system_text = tk.Text(self, height=4, width=50)
        self.system_text.pack()

        # User Role
        self.user_label = tk.Label(self, text="User Role")
        self.user_label.pack()
        self.user_text = tk.Text(self, height=4, width=50)
        self.user_text.pack()

        # Assistant Role
        self.assistant_label = tk.Label(self, text="Assistant Role")
        self.assistant_label.pack()
        self.assistant_text = tk.Text(self, height=4, width=50)
        self.assistant_text.pack()

        # Save Button
        self.save_button = tk.Button(self, text="Save Entry", command=self.save_entry)
        self.save_button.pack(pady=10)

        # Filename Entry
        self.filename_label = tk.Label(self, text="Filename (without extension)")
        self.filename_label.pack()
        self.filename_entry = tk.Entry(self)
        self.filename_entry.pack()

    def save_entry(self):
        system_role = self.system_text.get("1.0", tk.END).strip()
        user_role = self.user_text.get("1.0", tk.END).strip()
        assistant_role = self.assistant_text.get("1.0", tk.END).strip()

        if not system_role or not user_role or not assistant_role:
            messagebox.showwarning("Warning", "All fields must be filled out!")
            return

        entry = create_jsonl_entry(system_role, user_role, assistant_role)

        filename = self.filename_entry.get().strip()
        if not filename:
            messagebox.showwarning("Warning", "Filename must be provided!")
            return

        save_to_jsonl(filename + '.jsonl', entry)
        messagebox.showinfo("Success", "Entry saved successfully!")
        self.clear_fields()

    def clear_fields(self):
        # self.system_text.delete("1.0", tk.END)
        self.user_text.delete("1.0", tk.END)
        self.assistant_text.delete("1.0", tk.END)
        self.filename_entry.delete(0, tk.END)


# if __name__ == "__main__":
#     app = JsonlCreatorApp()
#     app.mainloop()
