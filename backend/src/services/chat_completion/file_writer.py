# Module: chat_completion/file_writer.py
# Description:
# Provides functionality to write chat completions to a .txt file.
# -----------------------------------------------------------------------------

class FileWriter:
    def __init__(self, file_path="latest_chat_completion.txt"):
        self.file_path = file_path

    def write_to_file(self, user_message, response):
        try:
            with open(self.file_path, "w", encoding="utf-8") as file:
                # file.write(f"User Message: \n\n{user_message}\n")
                file.write(f"Response: \n\n{response}\n")
            print(f"Latest chat completion saved to {self.file_path}")
        except IOError as e:
            print(f"Failed to write to file: {str(e)}")
