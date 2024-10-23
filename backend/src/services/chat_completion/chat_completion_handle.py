# Module: chat_completion/chat_completion_handle.py
# Description:
# Handles user interactions for chat completion services, including saving results to a Supabase table
# -----------------------------------------------------------------------------

import json
import logging
from pathlib import Path
from .chat_completion_manager import ChatCompletionManager
from .chat_completion_models import ChatMessage, ChatCompletionRequest
from .chat_completion_exceptions import ChatCompletionsRequestError, InvalidChatCompletionsModelError, \
    ServiceNotFoundError
from supabase_client import get_supabase_client

class ChatCompletionHandle:
    def __init__(self, config):
        self.chat_completion_manager = ChatCompletionManager(config)
        self.supabase = get_supabase_client()
        self.messages = []

    def delete_chat_history(self, email):
        """Delete all chat history for the given email from the Supabase table."""
        try:
            response = self.supabase.table('chat_histories').delete().eq('email', email).execute()
            if response.status_code == 200:
                print(f"All chat history for {email} has been deleted.")
            else:
                print(f"Failed to delete chat history for {email}. Status code: {response.status_code}")
        except Exception as e:
            print(f"An error occurred while deleting chat history: {str(e)}")
            
    def load_existing_responses(self, email):
        """Load existing responses from the Supabase table for the given email."""
        try:
            response = self.supabase.table('chat_histories').select('*').eq('email', email).execute()
            if response.data:
                for entry in response.data:
                    self.messages.append({"role": "user", "content": entry["user_message"]})
                    self.messages.append({"role": "assistant", "content": entry["response"]})
            else:
                logging.info("No previous conversation history found. Starting fresh.")
        except Exception as e:
            logging.error(f"Failed to load existing responses: {e}")
            print("An error occurred while loading the conversation history. Starting without history.")

    def create_chat_completion(self, email, user_message, max_tokens, model, temperature, stop, window_size):
        self.process_chat_completion(email, user_message, max_tokens, model, temperature, stop, window_size)

    def process_chat_completion(self, email, user_message, max_tokens, model, temperature, stop, window_size):
        try:
            chat_message = ChatMessage(role="user", content=user_message)
            self.messages.append({"role": "user", "content": user_message})

            # Ensure window_size is an integer
            window_size = int(window_size)

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

            # Save the result to Supabase
            self.save_result(email, user_message, model, max_tokens, temperature, stop, chat_completion_response)

            # Save the latest response to a file
            with open('latest_chat_completion.txt', 'w', encoding='utf-8') as file:
                file.write(chat_completion_response)

        except ChatCompletionsRequestError as e:
            print(f"Chat completions request error: {e.message} (Status code: {e.status_code})")
        except InvalidChatCompletionsModelError as e:
            print(f"Invalid chat completions model error: {str(e)}")
        except ServiceNotFoundError as e:
            print(f"Service not found error: {str(e)}")
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")

    def save_result(self, email, user_message, model, max_tokens, temperature, stop, response):
        try:
            result = {
                "email": email,
                "user_message": user_message,
                "model": model,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "stop": stop,
                "response": response
            }
            self.supabase.table('chat_histories').insert(result).execute()
            print("Result saved to Supabase")
        except Exception as e:
            print(f"Failed to save result: {str(e)}")

    def view_saved_results(self):
        if not self.messages:
            print("No results found. Generate some completions first.")
            return
        for i, message in enumerate(self.messages):
            print(f"\nMessage {i + 1}:")
            print(f"Role: {message['role']}")
            print(f"Content: {message['content']}")
        if not self.messages:
            return "No results found. Generate some completions first."
        return self.messages