# Module: chat_completion/chat_completion_handle.py
# Description:
# Handles user interactions for chat completion services, including saving results to a JSON file
# and the latest result to a .txt file.
# -----------------------------------------------------------------------------

import json
import logging
from pathlib import Path
from .chat_completion_manager import ChatCompletionManager
from .chat_completion_models import ChatMessage, ChatCompletionRequest
from .chat_completion_exceptions import ChatCompletionsRequestError, InvalidChatCompletionsModelError, \
    ServiceNotFoundError
from .file_writer import FileWriter


class ChatCompletionHandle:
    def __init__(self, config):
        self.chat_completion_manager = ChatCompletionManager(config)
        self.results_file = "chat_completion_results.json"
        self.results = self.load_results()
        self.file_writer = FileWriter()
        self.responses_file = Path(self.results_file)  # Path for the saved responses file
        self.messages = []
        self.load_existing_responses()  # Load existing responses upon initialization

    def load_existing_responses(self):
        """Load existing responses from the JSON file."""
        if self.responses_file.exists():
            try:
                with open(self.responses_file, 'r', encoding="utf-8") as file:
                    data = json.load(file)
                for entry in data:
                    if "user_message" in entry and "response" in entry:
                        self.messages.append({"role": "user", "content": entry["user_message"]})
                        self.messages.append({"role": "assistant", "content": entry["response"]})
                    else:
                        logging.error("Invalid entry format in JSON file.")
            except Exception as e:
                logging.error(f"Failed to load existing responses: {e}")
                print("An error occurred while loading the conversation history. Starting without history.")
        else:
            logging.info("No previous conversation history found. Starting fresh.")

    def create_chat_completion(self):
        user_message, max_tokens, model, temperature, stop, window_size = self.get_chat_completion_parameters()
        self.process_chat_completion(user_message, max_tokens, model, temperature, stop, window_size)

    def get_chat_completion_parameters(self):
        user_message = input("\nEnter your message for the chat completion: ")
        max_tokens = int(input("Enter the maximum number of tokens: "))
        model = input("Enter the model (e.g., gpt-3.5-turbo): ")
        temperature = input("Enter the temperature (default is 1.0): ")
        temperature = float(temperature) if temperature else 1.0
        stop = input("Enter the stop sequence (optional): ") or None
        window_size = int(input("Enter the window size for the history: "))
        return user_message, max_tokens, model, temperature, stop, window_size

    def process_chat_completion(self, user_message, max_tokens, model, temperature, stop, window_size):
        try:
            chat_message = ChatMessage(role="user", content=user_message)
            self.messages.append({"role": "user", "content": user_message})

            # Use only the most recent 'window_size' number of messages for context
            context_messages = self.messages[-(window_size * 2):]
            logging.debug("Messages to send: %s", context_messages)

            chat_completion_request = ChatCompletionRequest(
                model=model,
                messages=context_messages,  # Include the entire history of messages
                max_tokens=max_tokens,
                temperature=temperature,
                stop=stop
            )
            chat_completion_response = self.chat_completion_manager.create_chat_completion(chat_completion_request)
            print("\nChat Completion Response:")
            print(chat_completion_response)

            # Adding to messages for future requests
            self.messages.append({"role": "assistant", "content": chat_completion_response})

            # Save the result to JSON
            self.save_result(user_message, model, max_tokens, temperature, stop, chat_completion_response)

            # Save the latest result to TXT
            self.file_writer.write_to_file(user_message, chat_completion_response)

        except ChatCompletionsRequestError as e:
            print(f"Chat completions request error: {e.message} (Status code: {e.status_code})")
        except InvalidChatCompletionsModelError as e:
            print(f"Invalid chat completions model error: {str(e)}")
        except ServiceNotFoundError as e:
            print(f"Service not found error: {str(e)}")
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")

    def save_result(self, user_message, model, max_tokens, temperature, stop, response):
        result = {
            "user_message": user_message,
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stop": stop,
            "response": response
        }
        self.results.append(result)
        try:
            with open(self.results_file, "w", encoding="utf-8") as file:
                json.dump(self.results, file, indent=4, ensure_ascii=False)
            print("Result saved to chat_completion_results.json")
        except IOError as e:
            print(f"Failed to save result: {str(e)}")

    def load_results(self):
        try:
            with open(self.results_file, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def view_saved_results(self):
        if not self.results:
            print("No results found. Generate some completions first.")
            return
        for i, result in enumerate(self.results):
            print(f"\nResult {i + 1}:")
            print(f"User Message: {result['user_message']}")
            print(f"Model: {result['model']}")
            print(f"Max Tokens: {result['max_tokens']}")
            print(f"Temperature: {result['temperature']}")
            print(f"Stop: {result['stop']}")
            print(f"Response: {result['response']}")
