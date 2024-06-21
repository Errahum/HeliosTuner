import tkinter as tk
from tkinter import scrolledtext, font
import threading

from ..services.chat_completion.chat_completion_handle import ChatCompletionHandle


class OpenAIInterface(tk.Frame):
    def __init__(self, config):
        super().__init__()
        # self.root = root
        # self.root.title("Interface OpenAI")
        self.pack()

        # Attributs par défaut
        self.default_model = "gpt-3.5-turbo"
        self.default_max_tokens = 200
        self.default_temperature = 0.7
        self.default_windows = 5
        self.default_message = "Find the roots of a quadratic equation ax^2 + bx + c = 0."

        # Initialiser le handle de ChatCompletion
        self.config = config  # Vous pouvez configurer ce dictionnaire selon vos besoins
        self.chat_completion_handle = ChatCompletionHandle(self.config)

        # Définir la police
        self.custom_font = font.Font(family="Arial", size=14)

        # Fonction de validation pour autoriser tous les caractères
        def validate_all(text):
            return True

        # Champ d'entrée pour le message
        tk.Label(self, text="Message:", font=self.custom_font).grid(row=0, column=0, sticky=tk.W)
        self.input_text = scrolledtext.ScrolledText(self, width=80, height=10, wrap=tk.WORD, font=self.custom_font)
        self.input_text.insert(tk.END, self.default_message)
        self.input_text.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W)

        # Cadre pour les paramètres à droite
        self.params_frame = tk.Frame(self)
        self.params_frame.grid(row=1, column=2, rowspan=5, padx=10, pady=5, sticky=tk.N)

        # Champ d'entrée pour max_tokens
        tk.Label(self.params_frame, text="Max Tokens:", font=self.custom_font).grid(row=0, column=0, sticky=tk.W)
        self.max_tokens_entry = tk.Entry(self.params_frame, font=self.custom_font)
        self.max_tokens_entry.grid(row=0, column=1, padx=5, pady=5)
        self.max_tokens_entry.insert(tk.END, str(self.default_max_tokens))
        self.max_tokens_entry.config(validate="key", validatecommand=(self.register(validate_all), "%S"))

        # Champ d'entrée pour le modèle utilisé
        tk.Label(self.params_frame, text="Model:", font=self.custom_font).grid(row=1, column=0, sticky=tk.W)
        self.model_entry = tk.Entry(self.params_frame, font=self.custom_font)
        self.model_entry.grid(row=1, column=1, padx=5, pady=5)
        self.model_entry.insert(tk.END, self.default_model)
        self.model_entry.config(validate="key", validatecommand=(self.register(validate_all), "%S"))

        # Champ d'entrée pour la température
        tk.Label(self.params_frame, text="Temperature:", font=self.custom_font).grid(row=2, column=0, sticky=tk.W)
        self.temperature_scale = tk.Scale(self.params_frame, from_=0.1, to=1.0, resolution=0.01, orient=tk.HORIZONTAL)
        self.temperature_scale.grid(row=2, column=1, padx=5, pady=5)
        self.temperature_scale.set(self.default_temperature)

        # Champ d'entrée pour Stop Sequence
        tk.Label(self.params_frame, text="Stop Sequence:", font=self.custom_font).grid(row=3, column=0, sticky=tk.W)
        self.stop_sequence_entry = tk.Entry(self.params_frame, font=self.custom_font)
        self.stop_sequence_entry.grid(row=3, column=1, padx=5, pady=5)
        self.stop_sequence_entry.insert(tk.END, "")  # Valeur par défaut
        self.stop_sequence_entry.config(validate="key", validatecommand=(self.register(validate_all), "%S"))

        # Champ d'entrée pour la fenêtre pour l'historique
        tk.Label(self.params_frame, text="Windows history:", font=self.custom_font).grid(row=4, column=0, sticky=tk.W)
        self.windows_entry = tk.Entry(self.params_frame, font=self.custom_font)
        self.windows_entry.grid(row=4, column=1, padx=5, pady=5)
        self.windows_entry.insert(tk.END, str(self.default_windows))
        self.windows_entry.config(validate="key", validatecommand=(self.register(validate_all), "%S"))

        # Bouton pour envoyer la requête
        self.send_button = tk.Button(self.params_frame, text="Send", command=self.send_request, font=self.custom_font)
        self.send_button.grid(row=5, column=0, columnspan=2, padx=5, pady=10)

        # Champ de texte pour afficher le résultat
        tk.Label(self, text="Output:", font=self.custom_font).grid(row=2, column=0, sticky=tk.W)
        self.output_text = scrolledtext.ScrolledText(self, width=80, height=20, wrap=tk.WORD, font=self.custom_font)
        self.output_text.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W)

    def send_request(self):
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, "Veuillez patienter, la réponse est en cours...")

        def send_request_thread():
            user_message = self.input_text.get("1.0", tk.END).strip()
            max_tokens = int(self.max_tokens_entry.get())
            model = self.model_entry.get()
            temperature = float(self.temperature_scale.get())
            stop = self.stop_sequence_entry.get()
            if stop == "":
                stop = None
            else:
                stop = stop.strip()
            window_size = int(self.windows_entry.get())

            try:
                self.chat_completion_handle.process_chat_completion(
                    user_message, max_tokens, model, temperature, stop, window_size
                )
                response = self.read_latest_response_from_file()

                # Assurer que response est une chaîne de caractères
                if not isinstance(response, str):
                    response = str(response)

                self.output_text.delete("1.0", tk.END)
                self.output_text.insert(tk.END, response)
            except Exception as e:
                self.output_text.delete("1.0", tk.END)
                self.output_text.insert(tk.END, f"Une erreur est survenue: {str(e)}")

        # Exécuter send_request_thread dans un thread séparé
        thread = threading.Thread(target=send_request_thread)
        thread.start()

    def read_latest_response_from_file(self):
        try:
            with open("latest_chat_completion.txt", "r", encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError:
            return "latest_chat_completion.txt not found. Verify your API key or URL."
        except Exception as e:
            return f"Erreur lors de la lecture du fichier: {str(e)}"
