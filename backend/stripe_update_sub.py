import time
from supabase import create_client, Client
import os
from dotenv import load_dotenv
import stripe
import json
import logging

load_dotenv()

# Configurez votre clé API Stripe
stripe.api_key = os.getenv("stripe_key_backend")

valid_statuses = [
    'succeeded', 'paid', 'pending', 'failed', 'canceled',
    'requires_payment_method', 'requires_confirmation',
    'requires_action', 'processing', 'requires_capture', 'active'
]

def get_supabase_client():
    supabase_url: str  = os.getenv("SUPABASE_URL")
    supabase_key: str  = os.getenv("SUPABASE_SERVICE_KEY")
    supabase: Client = create_client(supabase_url, supabase_key)
    return supabase

def load_payment_links():
    with open('payment_links.json') as f:
        return json.load(f)

def get_price_id_and_max_tokens(price_id, payment_links):
    for plan_type in payment_links.values():
        if price_id in plan_type:
            return plan_type[price_id]['id'], plan_type[price_id]['tokens']
    return None, None

def upsert_subscription_in_db(supabase, email, subscription_id, customer_id, status, price_id, max_tokens):
    if status not in valid_statuses:
        logging.error(f"Invalid status '{status}' received for subscription {subscription_id}. Defaulting to 'draft'.")
        status = 'draft'
    
    # Set status to 'paid' for Supabase if it is 'active' in Stripe
    if status == 'active':
        status = 'paid'

    data = {
        "email": email,
        "subscription_id": subscription_id,
        "customer_id": customer_id,
        "status": status,
        "price_id": price_id,
        "max_tokens": max_tokens,
        "created_at": time.strftime('%Y-%m-%d %H:%M:%S'),
        "updated_at": time.strftime('%Y-%m-%d %H:%M:%S')
    }

    # Check if a record with the same email already exists
    existing_record = supabase.table("subscriptions").select("*").eq("email", email).execute()
    if existing_record.data:
        # Update the existing record
        response = supabase.table("subscriptions").update(data).eq("email", email).execute()
    else:
        # Insert a new record
        response = supabase.table("subscriptions").insert(data).execute()

    return response

def check_and_update_subscriptions():
    supabase = get_supabase_client()
    payment_links = load_payment_links()

    # Récupérer tous les utilisateurs de la base de données Supabase
    response = supabase.table("subscriptions").select("*").execute()
    users = response.data

    # Créer un dictionnaire pour un accès rapide par subscription_id
    user_dict = {user['subscription_id']: user for user in users}

    # Récupérer tous les abonnements Stripe
    subscriptions = stripe.Subscription.list()

    for subscription in subscriptions.auto_paging_iter():
        subscription_id = subscription['id']
        customer_id = subscription['customer']
        status = subscription['status']
        email = stripe.Customer.retrieve(customer_id)['email']
        price_id, max_tokens = get_price_id_and_max_tokens(subscription['items']['data'][0]['price']['id'], payment_links)

        # Ensure the status is valid for Supabase
        if status not in valid_statuses:
            logging.error(f"Invalid status '{status}' received for subscription {subscription_id}. Defaulting to 'draft'.")
            status = 'draft'

        # Set status to 'paid' for Supabase if it is 'active' in Stripe
        supabase_status = 'paid' if status == 'active' else status

        upsert_subscription_in_db(supabase, email, subscription_id, customer_id, supabase_status, price_id, max_tokens)
        logging.info(f"Subscription {subscription_id} for user {email} upserted with status {supabase_status}.")

# if __name__ == "__main__":
#     check_and_update_subscriptions()