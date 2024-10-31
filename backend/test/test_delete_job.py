import os
from openai import OpenAI
import openai

api_key_fineur = os.getenv("OPENAI_API_KEY_FINEUR")
client = OpenAI(api_key=api_key_fineur)

def delete_fine_tuned_model(model_id):
    """
    Deletes a fine-tuned model using the OpenAI API.
    
    Parameters:
    model_id (str): The ID of the fine-tuned model to delete.
    """
    try:
        # Delete the fine-tuned model
        response = client.models.delete(model_id)
        
        print(f"Model {model_id} deleted successfully.")
        return response
    except openai.OpenAIError as e:
        if e.code == 'model_not_found':
            print(f"Error: The model '{model_id}' does not exist.")
        else:
            print(f"An error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def list_fine_tuned_models():
    """
    Lists all fine-tuned models using the OpenAI API.
    
    Returns:
    list: A list of fine-tuned model IDs.
    """
    try:
        response = client.models.list()
        model_ids = [model.id for model in response.data]
        print("Available fine-tuned models:")
        for model_id in model_ids:
            print(model_id)
        return model_ids
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Example usage
if __name__ == "__main__":
    model_id = "ft:gpt-3.5-turbo-0125:fineurai:ft-gpt-3-5-turbo-0125-fineurai-math-to-python-amzzzo9k:ANP8fkBi"
    delete_fine_tuned_model(model_id)
    # list_fine_tuned_models()