import tkinter as tk
from tkinter import font, ttk
from .fine_tuning_gui_util import OpenAiInterfaceUtils
from ... import OpenAIInterface
from ...services.fine_tuning.fine_tuning_handle import FineTuningHandle


class OpenAIInterfaceFT(tk.Tk):
    def __init__(self, config):
        super().__init__()
        self.title("Interface OpenAI")
        self.geometry("1500x950")

        self.config = config
        self.custom_font = font.Font(family="Arial", size=14)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")

        self.default_model = "gpt-3.5-turbo"
        self.default_training_data_path = ""

        '''
        Pour remplacer `tk.StringVar` par une autre méthode d'interface utilisateur comme Dear PyGui, 
        vous pouvez directement utiliser des variables Python pour stocker les valeurs des entrées utilisateur. 
        Voici comment vous pourriez procéder :
        
        1. **Initialiser les variables** :
           Remplacez `tk.StringVar` par des simples variables Python.
        
        2. **Utiliser des widgets de Dear PyGui** :
           Utilisez les widgets de Dear PyGui pour créer les champs d'entrée.
        
        3. **Mettre à jour les valeurs** :
           Utilisez des callbacks pour mettre à jour les variables Python lorsque l'utilisateur modifie les entrées.
        '''

        # Initialize the entries with default values
        self.model_entry = tk.StringVar(value=self.default_model)
        self.name_entry = tk.StringVar(value="custom-model")
        self.seed_entry = tk.StringVar(value="0")
        self.n_epochs_entry = tk.StringVar(value="auto")
        self.learning_rate_entry = tk.StringVar(value="auto")
        self.batch_size_entry = tk.StringVar(value="auto")
        self.job_ids_listbox = None

        # Initialize FineTuningHandle with placeholders
        self.finetuninghandle = FineTuningHandle(self.config, self.default_training_data_path, self.model_entry.get(),
                                                 self.name_entry.get(), self.seed_entry.get(),
                                                 self.n_epochs_entry.get(), self.learning_rate_entry.get(),
                                                 self.batch_size_entry.get())

        # Initialize util_interface
        self.util_interface = OpenAiInterfaceUtils(self, self.job_ids_listbox, self.finetuninghandle,
                                                   self.default_training_data_path, self.model_entry, self.name_entry,
                                                   self.seed_entry, self.n_epochs_entry, self.learning_rate_entry,
                                                   self.batch_size_entry)

        self.create_fine_tuning_frame()
        self.create_list_frame()
        OpenAIInterface(self.config)

    def create_fine_tuning_frame(self):
        self.fine_tuning_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.fine_tuning_frame, text="Create Fine-Tuning Job")

        def validate_all(text):
            return True

        self.params_frame = tk.Frame(self.fine_tuning_frame)
        self.params_frame.pack(padx=10, pady=10)

        tk.Label(self.params_frame, text="Training Data Path:", font=self.custom_font).grid(row=0, column=0, sticky=tk.W)
        self.training_data_path_entry = tk.Entry(self.params_frame, font=self.custom_font)
        self.training_data_path_entry.grid(row=0, column=1, padx=5, pady=5)
        self.training_data_path_entry.insert(tk.END, self.default_training_data_path)
        self.training_data_path_entry.config(validate="key", validatecommand=(self.register(validate_all), "%S"))

        self.browse_button = tk.Button(self.params_frame, text="Browse", command=self.util_interface.browse_training_data, font=self.custom_font)
        self.browse_button.grid(row=0, column=2, padx=5, pady=5)

        tk.Label(self.params_frame, text="Model:", font=self.custom_font).grid(row=1, column=0, sticky=tk.W)
        tk.Entry(self.params_frame, textvariable=self.model_entry, font=self.custom_font).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.params_frame, text="Name:", font=self.custom_font).grid(row=2, column=0, sticky=tk.W)
        tk.Entry(self.params_frame, textvariable=self.name_entry, font=self.custom_font).grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.params_frame, text="Seed:", font=self.custom_font).grid(row=3, column=0, sticky=tk.W)
        tk.Entry(self.params_frame, textvariable=self.seed_entry, font=self.custom_font).grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self.params_frame, text="Number of Epochs:", font=self.custom_font).grid(row=4, column=0, sticky=tk.W)
        tk.Entry(self.params_frame, textvariable=self.n_epochs_entry, font=self.custom_font).grid(row=4, column=1, padx=5, pady=5)

        tk.Label(self.params_frame, text="Learning Rate:", font=self.custom_font).grid(row=5, column=0, sticky=tk.W)
        tk.Entry(self.params_frame, textvariable=self.learning_rate_entry, font=self.custom_font).grid(row=5, column=1, padx=5, pady=5)

        tk.Label(self.params_frame, text="Batch Size:", font=self.custom_font).grid(row=6, column=0, sticky=tk.W)
        tk.Entry(self.params_frame, textvariable=self.batch_size_entry, font=self.custom_font).grid(row=6, column=1, padx=5, pady=5)

        button_frame = tk.Frame(self.fine_tuning_frame)
        button_frame.pack(padx=10, pady=10)

        self.send_button = tk.Button(button_frame, text="Send", command=self.util_interface.create_fine_tuning_job, font=self.custom_font)
        self.send_button.pack(side="left", padx=10, pady=10)

    def create_list_frame(self):
        self.list_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.list_frame, text="List Fine-Tuning Jobs")

        button_frame = ttk.Frame(self.list_frame)
        button_frame.pack(side="top", padx=10, pady=10)

        self.get_all_jobs_button = tk.Button(button_frame, text="Get All Job IDs", command=self.util_interface.display_job_ids, font=self.custom_font)
        self.get_all_jobs_button.pack(side="left", padx=10, pady=10)

        self.select_job_button = tk.Button(button_frame, text="Select/Copy Job IDs", command=self.util_interface.select_job_ids, font=self.custom_font)
        self.select_job_button.pack(side="left", padx=10, pady=10)

        self.select_name_button = tk.Button(button_frame, text="Select/Copy Names", command=self.util_interface.select_names, font=self.custom_font)
        self.select_name_button.pack(side="left", padx=10, pady=10)

        self.cancel_button = tk.Button(button_frame, text="Cancel Job", command=self.util_interface.cancel_job, font=self.custom_font)
        self.cancel_button.pack(side="left", padx=10, pady=10)

        self.job_ids_listbox = tk.Listbox(self.list_frame, height=5, width=200, font=self.custom_font)
        self.job_ids_listbox.pack(side="bottom", padx=10, pady=10)

        self.util_interface.job_ids_listbox = self.job_ids_listbox
        self.util_interface.training_data_path_entry = self.training_data_path_entry
