import tkinter as tk
from tkinter import filedialog, messagebox


class OpenAiInterfaceUtils:
    def __init__(self, root, job_ids_listbox, finetuninghandle, training_data_path_entry, model_entry, name_entry,
                 seed_entry, n_epochs_entry, learning_rate_entry, batch_size_entry):
        self.root = root
        self.job_ids_listbox = job_ids_listbox
        self.finetuninghandle = finetuninghandle

        self.training_data_path_entry = training_data_path_entry
        self.model_entry = model_entry
        self.name_entry = name_entry
        self.seed_entry = seed_entry
        self.n_epochs_entry = n_epochs_entry
        self.learning_rate_entry = learning_rate_entry
        self.batch_size_entry = batch_size_entry

    def browse_training_data(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.jsonl"), ("All files", "*.*")])
        if filename:
            self.training_data_path_entry.delete(0, tk.END)
            self.training_data_path_entry.insert(tk.END, filename)

    def create_fine_tuning_job(self):
        self.training_data_path = self.training_data_path_entry.get()
        self.model = self.model_entry.get()
        self.name = self.name_entry.get()
        self.seed = self.seed_entry.get()
        self.n_epochs = self.n_epochs_entry.get()
        self.learning_rate = self.learning_rate_entry.get()
        self.batch_size = self.batch_size_entry.get()

        self.finetuninghandle.set_parameter(self.training_data_path, self.model, self.name, self.seed, self.n_epochs,
                                            self.learning_rate, self.batch_size)

        self.selected_job_id = self.finetuninghandle.upload_training_file()
        self.finetuninghandle.create_fine_tuning_job()

    def cancel_job(self):
        if not self.selected_job_id:
            print("Please select a Job ID to cancel.")
            messagebox.showwarning("Warning", "Please select a Job ID to cancel.")
            return
        try:
            self.finetuninghandle.cancel_fine_tuning_job([self.selected_job_id])
            print(f"Job {self.selected_job_id} canceled successfully.")
            messagebox.showwarning("info", f"Job {self.selected_job_id} is probably cancelled if no error occurred.")
        except Exception as e:
            print(f"Failed to cancel job {self.selected_job_id}: {e}")
            messagebox.showerror("Error", "Failed to cancel job")

    def display_job_ids(self):
        job_ids = self.finetuninghandle.get_all_job_ids()
        if job_ids:
            self.job_ids_listbox.delete(0, tk.END)
            for job_id in job_ids:
                self.job_ids_listbox.insert(tk.END, job_id)
        else:
            self.job_ids_listbox.delete(0, tk.END)
            self.job_ids_listbox.insert(tk.END, "Failed to retrieve job IDs.")

    def select_job_ids(self):
        selected_index = self.job_ids_listbox.curselection()
        if len(selected_index) != 1:
            print("Please select exactly one Job ID.")
            messagebox.showwarning("Warning", "Please select exactly one Job ID.")

            return
        self.selected_job_id = self.job_ids_listbox.get(selected_index[0]).split(" - ")[-1].split(":")[-1].strip()
        self.copy_to_clipboard(self.selected_job_id)
        print(self.selected_job_id)
        messagebox.showinfo("selected", self.selected_job_id)


    def select_names(self):
        selected_index = self.job_ids_listbox.curselection()
        if len(selected_index) != 1:
            print("Please select exactly one name.")
            messagebox.showwarning("Warning", "Please select exactly one name.")
            return
        self.selected_name = self.job_ids_listbox.get(selected_index[0]).split("name: ")[1].split(" - ")[0]
        self.copy_to_clipboard(self.selected_name)
        print(self.selected_name)
        messagebox.showinfo("selected", self.selected_name)

    def copy_to_clipboard(self, text):
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            self.root.update()
        except tk.TclError:
            messagebox.showerror("Error", "Failed to copy to clipboard.")
