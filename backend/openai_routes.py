import json
import logging
import os
import time
import uuid 
from flask import Blueprint, request, jsonify, session
import requests
import supabase
from datetime import datetime
from limiter import limiter  # Importer l'instance de Limiter
import threading

from supabase_client import get_supabase_client
from src.services.fine_tuning.fine_tuning_handle import FineTuningHandle
from src.services.chat_completion.chat_completion_handle import ChatCompletionHandle
from src.utils.jsonl_creator.jsonl_creator import create_jsonl_entry, save_to_jsonl
from src import Config
from src.utils.custom_logging import logging_custom


logging_custom()

chat_completion_bp = Blueprint('chat_completion', __name__)
fine_tuning_bp = Blueprint('fine_tuning', __name__)
jsonl_bp = Blueprint('jsonl', __name__)

config = Config()  # Assurez-vous de fournir la configuration nécessaire
chat_completion_handle = ChatCompletionHandle(config)

# Initialiser la gestion du fine-tuning avec les arguments nécessaires
fine_tuning_handle = FineTuningHandle(config,
    training_data_path=config.training_data_path,
    model=config.model,
    name=config.name,
    seed=config.seed,
    n_epochs=config.n_epochs,
    learning_rate=config.learning_rate,
    batch_size=config.batch_size
)
total_tokens_used = 0
supabase = get_supabase_client()  # Get the supabase client

if not os.path.exists(config.TEMP_DIR):
    os.makedirs(config.TEMP_DIR)

def track_tokens(user_email, tokens_used):
    try:
        # Récupérer l'abonnement de l'utilisateur
        subscription = supabase.table('subscriptions').select('total_tokens_used', 'price_id').eq('email', user_email).execute()

        if not subscription.data:
            logging.error(f"No subscription found for user {user_email}")
            return

        # Convertir total_tokens_used en entier
        total_tokens_used = int(subscription.data[0].get('total_tokens_used', 0))
        total_tokens = total_tokens_used + int(tokens_used)  # Assurez-vous que tokens_used est un entier
        price_id = subscription.data[0].get('price_id')
        max_tokens = get_plan_tokens(price_id)

        response = supabase.table('subscriptions').upsert({
            'email': user_email,
            'total_tokens_used': total_tokens,
            'max_tokens': max_tokens,
            'last_used_at': datetime.utcnow().isoformat()
        }, on_conflict=['email']).execute()

        if not response.data:
            logging.error(f"Failed to upsert tokens for user {user_email}: {response}")
            return

        logging.info(f"Successfully upserted tokens for user {user_email}. Total tokens used: {total_tokens}")

    except Exception as e:
        logging.error(f"Error tracking tokens for {user_email}: {e}")
        raise

@jsonl_bp.route('/create', methods=['POST'])
def create_jsonl():
    try:
        data = request.json
        system_role = data.get('system_role')
        user_role = data.get('user_role')
        assistant_role = data.get('assistant_role')

        if not system_role or not user_role or not assistant_role:
            return jsonify({'error': 'All fields must be filled out!'}), 400

        entry = create_jsonl_entry(system_role, user_role, assistant_role)
        return jsonify({'entry': entry}), 200
    except Exception as e:
        logging.error(f"Error creating JSONL entry: {e}")
        return jsonify({'error': str(e)}), 500

@jsonl_bp.route('/save', methods=['POST'])
def save_jsonl():
    try:
        data = request.json
        filename = data.get('filename')
        entry = data.get('entry')

        if not filename or not entry:
            return jsonify({'error': 'Filename and entry must be provided!'}), 400

        save_to_jsonl(filename + '.jsonl', entry)
        return jsonify({'message': 'Entry saved successfully!'}), 200
    except Exception as e:
        logging.error(f"Error saving JSONL entry: {e}")
        return jsonify({'error': str(e)}), 500
    
# Function to check the fine-tuning job status
def check_fine_tuning_status(fine_tuning_handle, user_email, tokens_used):
    try:
        max_attempts = 30  # Maximum number of attempts (e.g., 60 attempts)
        attempts = 0
        while not fine_tuning_handle.is_job_complete() and attempts <= max_attempts:
            time.sleep(30)
            attempts += 1
            logging.info(f"Checking fine-tuning status for {user_email} - Attempt {attempts}")

        # Track tokens used after the job is complete
        tokens_used += int(fine_tuning_handle.get_total_tokens_used())
        track_tokens(user_email, tokens_used)
        logging.info(f"Fine-tuning completed successfully for {user_email}")
    except Exception as e:
        logging.error(f"Error checking fine-tuning status: {e}")



# Fine-tuning routes
@fine_tuning_bp.route('/start', methods=['POST'])
def start_fine_tuning():
    try:
        user_email = session.get('email')
        if not user_email:
            return jsonify({'error': 'No email in session'}), 400

        data = request.json
        
        # Liste des modèles bloqués
        blocked_models = [
            'gpt-4-turbo', 'gpt-4', 'gpt-4-32k', 'gpt-4-turbo-preview', 'gpt-4-vision-preview', 
            'gpt-4-turbo-2024-04-09', 'gpt-4-0314', 'gpt-4-32k-0314', 'gpt-4-32k-0613', 
            'chatgpt-4o-latest', 'gpt-4-turbo', 'gpt-4-turbo-2024-04-09', 'gpt-4', 'gpt-4-32k', 
            'gpt-4-0125-preview', 'gpt-4-1106-preview', 'gpt-4-vision-preview', 
            'gpt-4o-realtime-preview', 'gpt-4o-realtime-preview-2024-10-01', 'babbage-002', 
            'davinci-002', 'o1-preview-2024-09-12', 'o1-preview'
        ]

        # Vérifier si le modèle est bloqué
        if data['model'] in blocked_models:
            return jsonify({"error": "The selected model is not allowed."}), 403
        
        # Validate input data for fine-tuning parameters
        required_fields = ['model', 'name', 'seed', 'n_epochs', 'learning_rate', 'batch_size']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Retrieve the training data path from the session
        # Retrieve the training data path from the session
        training_data_path = session.get('training_data_path')
        if not training_data_path:
            return jsonify({'error': 'Training data path not found in session'}), 400

        # Ensure the training data path is a temporary file
        if not training_data_path.startswith(config.TEMP_DIR):
            return jsonify({'error': 'Invalid training data path'}), 400



        # Set the required token threshold
        tokens_needed = 1000  # Example threshold for fine-tuning

        # Check if user has enough tokens and a valid subscription
        is_allowed, message = check_quota(user_email, tokens_needed)
        if not is_allowed:
            return jsonify({'error': message}), 403

        # Check if the user has a valid subscription
        subscription = supabase.table('subscriptions').select('status').eq('email', user_email).execute()
        if not subscription.data or subscription.data[0]['status'] not in ('succeeded', 'paid'):
            return jsonify({'error': 'Invalid subscription status'}), 403

        # Vérifier que l'utilisateur est bien le créateur du modèle
        job_id = data.get('job_id')
        if job_id:
            job_metadata = supabase.table('fine_tuning_jobs').select('user_email').eq('job_id', job_id).execute()
            if not job_metadata.data or job_metadata.data[0]['user_email'] != user_email:
                return jsonify({'error': 'You are not authorized to modify this job'}), 403

        # Define the fine-tuning parameters
        fine_tuning_handle.set_parameter(
            training_data_path=training_data_path,
            model=data['model'],
            name=data['name'],
            seed=data['seed'],
            n_epochs=data['n_epochs'],
            learning_rate=data['learning_rate'],
            batch_size=data['batch_size']
        )



        # At this point, all conditions are satisfied, and we can start fine-tuning
        fine_tuning_handle.create_fine_tuning_job(user_email)
        logging.info("Fine-tuning started successfully")

        # Track tokens used during the process
        tokens_used = int(fine_tuning_handle.get_total_tokens_used())
        tokens_used += 100  # Example tokens used for fine-tuning


        # Periodically check the status of the fine-tuning job
        # max_attempts = 60  # Maximum number of attempts (e.g., 60 attempts)
        # attempts = 0
        # while not fine_tuning_handle.is_job_complete() and attempts < max_attempts:
        #     time.sleep(10)
        #     attempts += 1

        
        # Start a new thread to check the fine-tuning status
        status_thread = threading.Thread(target=check_fine_tuning_status, args=(fine_tuning_handle, user_email, tokens_used))
        status_thread.start()

        # Track tokens used after the job is complete
        tokens_used += int(fine_tuning_handle.get_total_tokens_used())
        track_tokens(user_email, tokens_used)

        logging.info(f"Fine-tuning completed successfully for {user_email}")
        return jsonify({'message': 'Fine-tuning started successfully'}), 200

    except Exception as e:
        logging.error(f"Error starting fine-tuning: {e}")
        return jsonify({'error': str(e)}), 500
    
@fine_tuning_bp.route('/delete-all-temp-files', methods=['POST'])
@limiter.exempt
def delete_all_temp_files():
    try:
        temp_dir = config.TEMP_DIR
        for filename in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
                logging.info(f"Temporary file deleted: {file_path}")
        return jsonify({'message': 'All temporary files deleted successfully'}), 200
    except Exception as e:
        logging.error(f"Error deleting all temporary files: {e}")
        return jsonify({'error': str(e)}), 500
    
@fine_tuning_bp.route('/delete-temp-file', methods=['POST'])
def delete_temp_file():
    try:
        data = request.json
        file_name = data.get('fileName')
        temp_file_path = os.path.join(config.TEMP_DIR, file_name)
        
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            logging.info(f"Temporary file deleted: {temp_file_path}")
            return jsonify({'message': 'Temporary file deleted successfully'}), 200
        else:
            return jsonify({'error': 'Temporary file not found'}), 404
    except Exception as e:
        logging.error(f"Error deleting temporary file: {e}")
        return jsonify({'error': str(e)}), 500
    
@fine_tuning_bp.route('/upload', methods=['POST'])
def upload_training_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400

        file = request.files['file']
        user_email = session.get('email')
        if not user_email:
            return jsonify({'error': 'User not in session'}), 401

        # Generate a unique temporary file name
        unique_filename = f"temp_{uuid.uuid4()}_{file.filename}"
        temp_file_path = os.path.join(config.TEMP_DIR, unique_filename)
        file.save(temp_file_path)
        
        # Moderation step
        with open(temp_file_path, 'rb') as f:
            file_content = f.read()
        moderation_result = moderate_content(file_content)
        if not moderation_result['is_safe']:
            logging.warning(f"File content failed moderation: {moderation_result['reason']}")
            os.remove(temp_file_path)  # Delete the temporary file
            return jsonify({'error': 'File content is not safe for fine-tuning', 'reason': moderation_result['reason']}), 400
        
        # Store the training data path in the session
        session['training_data_path'] = temp_file_path
        
        logging.info(f"File uploaded successfully: {file.filename}")
        return jsonify({'message': 'File uploaded successfully', 'training_data_path': temp_file_path}), 200
    except Exception as e:
        logging.error(f"Error uploading file: {e}")
        return jsonify({'error': str(e)}), 500

def moderate_content(content):
    try:
        url = "https://api.openai.com/v1/moderations"
        headers = {
            "Authorization": f"Bearer {config.get_api_key()}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "omni-moderation-latest",
            "input": content.decode('utf-8')
        }
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an error for bad status codes
        
        moderation_result = response.json()
        
        # Print the response to understand its structure
        logging.info(f"Moderation response: {moderation_result}")
        
        # Access the attributes correctly based on the response structure
        results = moderation_result['results'][0]
        if results['flagged']:
            # Increment the moderation count in the database
            user_email = session.get('email')
            if user_email:
                # Fetch the current moderation count
                current_record = supabase.table('subscriptions').select('moderation').eq('email', user_email).execute()
                current_moderation_count = current_record.data[0]['moderation'] if current_record.data else 0
                
                # Update the moderation count
                supabase.table('subscriptions').upsert({
                    'email': user_email,
                    'moderation': current_moderation_count + 1
                }, on_conflict=['email']).execute()
            return {'is_safe': False, 'reason': results['categories']}
        return {'is_safe': True, 'reason': None}
    except Exception as e:
        logging.error(f"Error during content moderation: {e}")
        return {'is_safe': False, 'reason': 'Moderation service error'}




@fine_tuning_bp.route('/jobs', methods=['GET'])
def get_all_jobs():
    try:
        job_ids = fine_tuning_handle.get_all_job_ids()
        logging.info("Fetched all job IDs successfully")
        return jsonify({'job_ids': job_ids}), 200
    except Exception as e:
        logging.error(f"Error fetching job IDs: {e}")
        return jsonify({'error': str(e)}), 500
    

@fine_tuning_bp.route('/jobs/cancel', methods=['POST'])
def cancel_job():
    try:
        user_email = session.get('email')
        if not user_email:
            return jsonify({'error': 'No email in session'}), 400

        job_id = request.json.get('job_id')
        
        # Récupérer les métadonnées du job pour vérifier l'email du créateur
        job_metadata = supabase.table('fine_tuning_jobs').select('user_email').eq('job_id', job_id).execute()
        if not job_metadata.data or job_metadata.data[0]['user_email'] != user_email:
            return jsonify({'error': 'You are not authorized to cancel this job'}), 403

        fine_tuning_handle.cancel_fine_tuning_job([job_id])
        logging.info(f"Job {job_id} cancelled successfully")
        return jsonify({'message': 'Job cancelled successfully'}), 200
    except Exception as e:
        logging.error(f"Error cancelling job {job_id}: {e}")
        return jsonify({'error': str(e)}), 500

with open('payment_links.json') as f:
    payment_links = json.load(f)

@fine_tuning_bp.route('/copy-model-name', methods=['POST'])
def copy_model_name():
    try:
        data = request.json
        job_info = data.get('job_info')
        if not job_info:
            return jsonify({'error': 'Job info must be provided!'}), 400

        # Extract the model name from the job info string using the new logic
        model_name = job_info.split("name: ")[1].split(" - ")[0].strip()

        return jsonify({'message': 'Model name copied successfully!', 'model_name': model_name}), 200
    except Exception as e:
        logging.error(f"Error copying model name: {e}")
        return jsonify({'error': str(e)}), 500

def get_plan_tokens(price_id):
    for plan_type in payment_links.values():
        if price_id in plan_type:
            return plan_type[price_id]['tokens']
    return 0

def check_quota(user_email, tokens_needed):
    try:
        # Récupérer l'abonnement de l'utilisateur
        subscription = supabase.table('subscriptions').select('price_id', 'total_tokens_used', 'max_tokens').eq('email', user_email).execute()

        if subscription.data:
            total_tokens_used = int(subscription.data[0].get('total_tokens_used', 0))
            max_tokens = int(subscription.data[0].get('max_tokens', 0))

            # Si `max_tokens` n'est pas défini, récupérer la valeur à partir du plan
            if not max_tokens or max_tokens == 0:
                price_id = subscription.data[0]['price_id']
                max_tokens = get_plan_tokens(price_id)

            # Vérifier si l'utilisateur a assez de tokens
            if total_tokens_used + int(tokens_needed) > max_tokens:
                return False, f"Quota exceeded. You have used {total_tokens_used} out of {max_tokens} tokens."
        
        return True, ""
    except Exception as e:
        logging.error(f"Error checking quota for {user_email}: {e}")
        return False, str(e)

# Chat completion routes
def moderate_content_completion(content):
    try:
        url = "https://api.openai.com/v1/moderations"
        headers = {
            "Authorization": f"Bearer {config.get_api_key()}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "omni-moderation-latest",
            "input": content  # No need to decode
        }
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an error for bad status codes
        
        moderation_result = response.json()
        
        # Print the response to understand its structure
        logging.info(f"Moderation response: {moderation_result}")
        
        # Access the attributes correctly based on the response structure
        results = moderation_result['results'][0]
        if results['flagged']:
            # Increment the moderation count in the database
            user_email = session.get('email')
            if user_email:
                # Fetch the current moderation count
                current_record = supabase.table('subscriptions').select('moderation').eq('email', user_email).execute()
                current_moderation_count = current_record.data[0]['moderation'] if current_record.data else 0
                
                # Update the moderation count
                supabase.table('subscriptions').upsert({
                    'email': user_email,
                    'moderation': current_moderation_count + 1
                }, on_conflict=['email']).execute()
            return {'is_safe': False, 'reason': results['categories']}
        return {'is_safe': True, 'reason': None}
    except Exception as e:
        logging.error(f"Error during content moderation: {e}")
        return {'is_safe': False, 'reason': 'Moderation service error'}


@chat_completion_bp.route('/create', methods=['POST'])
def create_chat_completion():
    try:
        data = request.json
        email = session.get('email')  # Récupérer l'email de la session
        if not email:
            return jsonify({"error": "Email not found in session"}), 400

        user_message = data.get('user_message')
        max_tokens = data.get('max_tokens')
        model = data.get('model')
        temperature = data.get('temperature')
        stop = data.get('stop')
        window_size = data.get('window_size')

        # Liste des modèles bloqués
        blocked_models = [
            'gpt-4-turbo', 'gpt-4', 'gpt-4-32k', 'gpt-4-turbo-preview', 'gpt-4-vision-preview', 
            'gpt-4-turbo-2024-04-09', 'gpt-4-0314', 'gpt-4-32k-0314', 'gpt-4-32k-0613', 
            'chatgpt-4o-latest', 'gpt-4-turbo', 'gpt-4-turbo-2024-04-09', 'gpt-4', 'gpt-4-32k', 
            'gpt-4-0125-preview', 'gpt-4-1106-preview', 'gpt-4-vision-preview', 
            'gpt-4o-realtime-preview', 'gpt-4o-realtime-preview-2024-10-01', 'babbage-002', 
            'davinci-002', 'o1-preview-2024-09-12', 'o1-preview'
        ]

        # Vérifier si le modèle est bloqué
        if model in blocked_models:
            return jsonify({"error": "The selected model is not allowed."}), 403

        # Définir le seuil de tokens requis
        tokens_needed = max_tokens  # Seuil pour la création de chat completion

        # Vérifier si l'utilisateur a suffisamment de tokens et un abonnement valide
        is_allowed, message = check_quota(email, tokens_needed)
        if not is_allowed:
            return jsonify({'error': message}), 403

        # Vérifier si l'utilisateur a un abonnement valide
        subscription = supabase.table('subscriptions').select('status').eq('email', email).execute()
        if not subscription.data or subscription.data[0]['status'] not in ('succeeded', 'paid'):
            return jsonify({'error': 'User does not have an active subscription'}), 403

        # Appel à la fonction de modération
        moderation_result = moderate_content_completion(user_message)
        if not moderation_result['is_safe']:
            return jsonify({"error": "Message contains inappropriate content", "reason": moderation_result['reason']}), 400

        print("Message is safe for chat completion")
        chat_completion_handle.create_chat_completion(email, user_message, max_tokens, model, temperature, stop, window_size)

        # Suivre les tokens utilisés après la création du chat completion
        track_tokens(email, tokens_needed)

        return jsonify({"message": "Chat completion created successfully"}), 200
    except Exception as e:
        logging.error(f"Error creating chat completion: {e}")
        return jsonify({"error": str(e)}), 500
    

@chat_completion_bp.route('/view', methods=['GET'])
def view_saved_results():
    try:
        email = session.get('email')  # Récupérer l'email de la session
        if not email:
            return jsonify({"error": "Email not found in session"}), 400

        chat_completion_handle.load_existing_responses(email)
        results = chat_completion_handle.view_saved_results()
        return jsonify(results), 200
    except Exception as e:
        logging.error(f"Error viewing saved results: {e}")
        return jsonify({"error": str(e)}), 500
    
@chat_completion_bp.route('/response', methods=['GET'])
def get_latest_response():
    try:
        # Assuming the latest response is stored in a file or a database
        with open('latest_chat_completion.txt', 'r', encoding='utf-8') as file:
            latest_response = file.read()
        return jsonify({"response": latest_response}), 200
    except FileNotFoundError:
        return jsonify({"error": "latest_chat_completion.txt not found. Verify your API key or URL."}), 404
    except Exception as e:
        logging.error(f"Error fetching latest response: {e}")
        return jsonify({"error": str(e)}), 500
    
@fine_tuning_bp.route('/jobs/<job_id>/status', methods=['GET'])
def get_job_status(job_id):
    try:
        if not job_id or job_id == 'undefined':
            return jsonify({'error': 'Invalid job ID'}), 400

        status = fine_tuning_handle.get_job_status(job_id)
        return jsonify({'status': status})
    except Exception as e:
        logging.error(f"Error getting job status: {e}")
        return jsonify({'error': str(e)}), 500
    
@chat_completion_bp.route('/delete-chat-history', methods=['POST'])
def delete_chat_history():
    try:
        user_email = session.get('email')
        if not user_email:
            return jsonify({"error": "User not authenticated"}), 401

        chat_completion_handle.delete_chat_history(user_email)
        return jsonify({"message": f"Chat history for {user_email} has been deleted."}), 200
    except Exception as e:
        logging.error(f"Error deleting chat history for {user_email}: {e}")
        return jsonify({"error": "An error occurred while deleting chat history"}), 500