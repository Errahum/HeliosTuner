from email.mime.text import MIMEText
import smtplib
from flask import Flask, request, jsonify, session
import jwt
import os
from dotenv import load_dotenv
import stripe
import re
import json
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
import traceback
from datetime import datetime, timedelta
import logging

# Ajoutez le chemin du dossier backend au PYTHONPATH
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from stripe_cancel_sub import cancel_all_subscriptions, get_customer_ids_by_email
from supabase_client import get_supabase_client
from openai_routes import fine_tuning_bp, chat_completion_bp, get_plan_tokens, jsonl_bp
from src.utils.custom_logging import logging_custom

logging_custom()

app = Flask(__name__)

load_dotenv()  # Charger les variables d'environnement à partir du fichier .env 

app.secret_key = os.getenv("SECRET_KEY")  # Add a secret key for session management
serializer = URLSafeTimedSerializer(os.getenv("SECRET_KEY"))

supabase = get_supabase_client()

stripe.api_key = os.getenv('stripe_key_test_backend')

stripe.api_key = str(os.getenv("stripe_key_test_backend"))# Initialiser la gestion du chat


PRODUCT_ID = (os.getenv("stripe_product_ID"))  # Remplacez par l'ID de votre produit


# -------------------------Product--------------------------------

try:

    app.register_blueprint(fine_tuning_bp, url_prefix='/api/fine-tuning')
    app.register_blueprint(chat_completion_bp, url_prefix='/api/chat-completion')
    app.register_blueprint(jsonl_bp, url_prefix='/api/jsonl')

except Exception as e:
    logging.error(f"Error product: {e}")


# ---------------------------Account-------------------------------------

import json  # Assurez-vous que le module json est importé

@app.route('/api/get-subscription-info', methods=['GET'])
def get_subscription_info():
    email = session.get('email')
    if not email:
        return jsonify({'error': 'User not logged in'}), 401

    try:
        response = supabase.table('subscriptions').select('*').eq('email', email).execute()
        if not response.data:
            return jsonify({'error': 'No subscription info found'}), 404

        data = response.data
        subscription_info = data[0]  # Assuming the response data is a list of subscriptions

        # Récupérer le price_id de l'abonnement
        price_id = subscription_info.get('price_id')

        # Trouver le nom de l'abonnement dans payment_links.json
        subscription_name = None
        for plan_type in payment_links.values():
            if price_id in plan_type:
                subscription_name = plan_type[price_id]['name']
                break

        # Récupérer les informations d'abonnement depuis Stripe
        stripe_subscription = stripe.Subscription.retrieve(subscription_info['subscription_id'])
        current_period_start = datetime.fromtimestamp(stripe_subscription['current_period_start'])
        current_period_end = datetime.fromtimestamp(stripe_subscription['current_period_end'])
        days_until_renewal = (current_period_end - datetime.utcnow()).days

        return jsonify({
            'subscriptionPlan': subscription_name,
            'nextPaymentDate': current_period_end.isoformat(),
            'billingCycle': f"{current_period_start.strftime('%B %d')} - {current_period_end.strftime('%B %d')}",
            'daysUntilRenewal': days_until_renewal
        })
    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({'error': str(e)}), 500
    


@app.route('/api/cancel-subscription', methods=['POST'])
def cancel_subscription():
    email = session.get('email')
    if not email:
        logging.error(f"Error User not logged in")
        return jsonify({'error': 'User not logged in'}), 401

    try:
        cancel_all_subscriptions(email)
        logging.error(f"Subscription cancelled successfully")
        return jsonify({'message': 'Subscription cancelled successfully'})
    except Exception as e:
        logging.error(f"error: {e}")
        return jsonify({'error': str(e)}), 500
    
# -------------------------contact-us---------------------------------------

smtp_host = os.getenv('SMTP_HOST')
smtp_port = int(os.getenv('SMTP_PORT'))
username = os.getenv('SMTP_USERNAME')
password = os.getenv('SMTP_PASSWORD')
to_email = os.getenv('SMTP_TO_EMAIL')

@app.route('/api/contact-us', methods=['POST'])
def contact_us():
    if 'email' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.json
    subject = data.get('subject')
    email = data.get('email')
    message = data.get('message')

    if not subject or not email or not message:
        return jsonify({'error': 'All fields are required'}), 400

    msg = MIMEText(f"Subject: {subject}\nEmail: {email}\nMessage: {message}")
    msg['Subject'] = 'Contact Us Form Submission'
    msg['From'] = username
    msg['To'] = to_email

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
            server.login(username, password)
            server.sendmail(username, to_email, msg.as_string())
        return jsonify({'message': 'Email sent successfully!'}), 200
    except Exception as e:
        logging.error(f"Error sending email: {e}")
        return jsonify({'error': str(e)}), 500
    
# ----------------------------------------------------------------

@app.route('/api/user-info', methods=['GET'])
def get_user_info():
    try:
        email = session.get('email')
        user_id = session.get('user_id')  # Assuming user_id is stored in session
    except Exception as e:
        logging.error(f"Error retrieving session data: {e}")
        return jsonify({'error': 'Internal server error'}), 500

    if not email:
        logging.error("User not logged in")
        return jsonify({'error': 'User not logged in'}), 400

    return jsonify({'email': email, 'user_id': user_id})


@app.route('/api/get-tokens', methods=['GET'])
def get_tokens():
    email = session.get('email')
    if not email:
        return jsonify({'error': 'No email in session'}), 400

    try:
        subscription = supabase.table('subscriptions').select('total_tokens_used', 'price_id', 'status').eq('email', email).execute()
        
        if subscription.data:
            subscription_data = subscription.data[0]
            total_tokens_used = subscription_data.get('total_tokens_used')
            price_id = subscription_data.get('price_id')
            status = subscription_data.get('status')

            if total_tokens_used is None or price_id is None or status is None:
                logging.error(f"Missing data in subscription response for {email}: {subscription.data}")
                return jsonify({'error': 'Incomplete subscription data'}), 500

            if status not in ('succeeded', 'paid'):
                return jsonify({'tokens': 0, 'max_tokens': 0}), 200

            # Trouver le nombre de tokens maximum pour le plan
            max_tokens = None
            for plan_type in payment_links.values():
                for plan in plan_type.values():
                    if plan['id'] == price_id:
                        max_tokens = plan['tokens']
                        break

            if max_tokens is not None:
                remaining_tokens = max_tokens - total_tokens_used
                return jsonify({'tokens': remaining_tokens, 'max_tokens': max_tokens}), 200
            else:
                return jsonify({'error': 'Plan not found'}), 404
        else:
            return jsonify({'error': 'Subscription not found'}), 404
    except Exception as e:
        logging.error(f"Error fetching tokens for {email}: {e}")
        return jsonify({'error': str(e)}), 500
    

# ------------------------- Magic Link--------------------------------



def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

@app.route('/api/send-magic-link', methods=['POST'])
def send_magic_link():
    data = request.json
    email = data.get('email')
    if not email:
        return jsonify({"message": "Email is required"}), 400

    if not is_valid_email(email):
        return jsonify({"message": "Invalid email format"}), 400

    try:
        send_magic_link_to_email(email)
        return jsonify({"message": "Magic link sent!"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
 
def send_magic_link_to_email(email):
    try:
        # Générer un token avec itsdangerous (expirant après 10 minutes)
        token = serializer.dumps(email, salt='email-confirm-salt')

        port = int(os.getenv("PORT", 5000))
        if port == 5000:
            link = f"http://localhost:3000/payment?token={token}&email={email}"
        else:
            link = f"https://fineurai.com/payment?token={token}&email={email}"
        # Construire le lien avec le token
        

        # Envoyer l'email via Supabase (utilisation d'OTP pour un lien de connexion magique)
        response = supabase.auth.sign_in_with_otp({
            "email": email,
            "options": {
                "email_redirect_to": link  # URL de redirection avec le token itsdangerous
            }
        })

        # Vérifier si l'envoi de l'email a réussi
        if 'error' in response:
            raise Exception(f"Error sending email: {response['error']['message']}")
        
        logging.info(f"Magic link sent to {email} with URL: {link}")
    except Exception as e:
        logging.error(f"Error sending magic link: {e}")
        logging.error(traceback.format_exc())
        
        raise
def generate_jwt(email):
    payload = {
        'email': email,
        'exp': datetime.utcnow() + timedelta(hours=24)  # Token valid for 24 hours
    }
    token = jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm='HS256')
    return token

@app.route('/api/check-session', methods=['GET'])
def check_session():
    jwt_token = session.get('jwt_token')

    if not jwt_token:
        return jsonify({"message": "No active session"}), 401

    try:
        decoded_token = jwt.decode(jwt_token, os.getenv("SECRET_KEY"), algorithms=['HS256'])
        return jsonify({"message": "Session valid", "email": decoded_token['email']}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Session expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid session"}), 401


@app.route('/api/verify-magic-link', methods=['POST'])
def verify_magic_link():
    data = request.json
    email = data.get('email')
    token = data.get('token')

    if not email or not token:
        return jsonify({"message": "Email and token are required"}), 400

    try:
        email_from_token = serializer.loads(token, salt='email-confirm-salt', max_age=86400)  # 24 heures
        logging.info(f"Email from token: {email_from_token}, Provided email: {email}")
        
        if email_from_token == email:
            # Vérifier si l'email existe déjà dans la base de données
            response = supabase.table('subscriptions').select('email').eq('email', email).execute()
            logging.info(f"Supabase select response: {response.data}")
            
            if response.data:  # Utiliser l'attribut .data pour accéder aux données
                logging.info(f"Email {email} already exists in the database.")
                
                # Generate JWT token
                jwt_token = generate_jwt(email)
                
                # Store JWT token in session or return it in response
                session['jwt_token'] = jwt_token

                session['email'] = email
                return jsonify({"message": "Magic link verified successfully!", "token": jwt_token}), 200

            # Convertir les objets datetime en chaînes de caractères
            created_at = datetime.utcnow().isoformat()
            updated_at = datetime.utcnow().isoformat()

            # Ajout de l'email dans la base de données Supabase
            response = supabase.table('subscriptions').insert({
                'email': email,
                'created_at': created_at,
                'updated_at': updated_at
            }).execute()

            logging.info(f"Supabase insert response: {response}")
            if not response.data:  # Utiliser l'attribut .data pour accéder aux données
                raise Exception(f"Erreur d'insertion : {response}")

            # Generate JWT token
            jwt_token = generate_jwt(email)
            
            # Store JWT token in session or return it in response
            session['jwt_token'] = jwt_token
            
            return jsonify({"message": "Magic link verified successfully!", "token": jwt_token}), 200
        else:
            return jsonify({"message": "Invalid email or token"}), 400
    except SignatureExpired:
        return jsonify({"message": "Token expired"}), 400
    except BadSignature:
        return jsonify({"message": "Invalid token"}), 400
    except Exception as e:
        logging.error(f"Error verifying magic link: {e}")
        logging.error(traceback.format_exc())
        return jsonify({"message": "An error occurred while verifying the magic link"}), 500


@app.route('/api/get-offers', methods=['GET'])
def get_offers():
    try:
        # Récupérer le produit spécifique
        product = stripe.Product.retrieve(PRODUCT_ID)
        logging.info(f"Product: {product}")  # Vérifiez le produit récupéré
        
        # Récupérer les prix associés au produit
        prices = stripe.Price.list(product=PRODUCT_ID)
        logging.info(f"Prices for product {PRODUCT_ID}: {prices}")  # Vérifiez les prix récupérés
        
        offers = []
        for price in prices['data']:
            offers.append({
                'id': price['id'],
                'name': product['name'],
                'description': product['description'],
                'price': price['unit_amount'] / 100,  # Convertir en dollars/euros
                'currency': price['currency']
            })
        
        logging.info(f"Offers: {offers}")  # Ajoutez cette ligne pour vérifier les données
        return jsonify({'offers': offers}), 200
    except Exception as e:
        logging.error(f"Error: {e}")  # Ajoutez cette ligne pour vérifier les erreurs
        return jsonify({'error': str(e)}), 500
    
with open('payment_links.json') as f:
    payment_links = json.load(f)

@app.route('/api/payment-links', methods=['GET'])
def get_payment_links():
    return jsonify(payment_links)

@app.route('/api/create-payment-link', methods=['POST'])
def create_payment_link():
    data = request.json
    try:
        # Log the incoming data
        logging.info(f"Received data for payment link: {data}")

        # Check if price_id is present
        if 'price_id' not in data:
            raise ValueError("Missing 'price_id' in request data")

        # Log the price_id
        logging.info(f"Using price_id: {data['price_id']}")

        # Create a Payment Link using Stripe API
        payment_link = stripe.PaymentLink.create(
            line_items=[{'price': data['price_id'], 'quantity': 1}]
        )

        # Log the Payment Link URL
        logging.info(f"Created payment link: {payment_link.url}")

        return jsonify({'url': payment_link.url}), 200
    except Exception as e:
        # Log the error
        logging.error(f"Error creating payment link: {e}")
        return jsonify({'error': str(e)}), 500
    



# ----------------------------------------------------------------


# ------------------------- Subscription logic --------------------------------




@app.route('/api/create-subscription', methods=['POST'])
def create_subscription():
    data = request.json
    email = data.get('email')
    price_id = data.get('price_id')

    if not email or not price_id:
        return

    try:
        # Créer un client Stripe avec l'email fourni
        customer = stripe.Customer.create(email=email)

        # Créer un abonnement Stripe avec le customer et price_id
        subscription = stripe.Subscription.create(
            customer=customer.id,
            items=[{'price': price_id}],
            expand=['latest_invoice.payment_intent']
        )

        # Appeler update_subscription_in_db pour gérer la mise à jour ou l'insertion dans la base de données
        update_subscription_in_db(subscription.id, email, customer.id, price_id, subscription.status)

        return
    except Exception as e:
        logging.error(f"Error creating subscription: {e}")
        return





def update_subscription_in_db(subscription_id, email, customer_id, price_id, status):
    try:
        # Convertir les statuts pour correspondre aux valeurs attendues
        status = "canceled" if status == "canceled" else "active"

        # Récupérer le nombre de tokens pour le plan sélectionné
        max_tokens = get_plan_tokens(price_id)  # Initialiser max_tokens ici

        # Utiliser UPSERT pour insérer ou mettre à jour en cas de conflit sur l'email
        response = supabase.table('subscriptions').upsert({
            'subscription_id': subscription_id,
            'email': email,
            'customer_id': customer_id,
            'price_id': price_id,
            'status': status,
            'total_tokens_used': 0,  # Initialiser les tokens utilisés à 0
            'max_tokens': max_tokens,  # Initialiser max_tokens à partir du plan
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }, on_conflict=['email']).execute()

        # Vérifier si l'opération a réussi
        if response.get('status_code') not in [200, 201]:
            raise Exception(f"Failed to insert/update data: {response.get('data')}")

        logging.info(f"Subscription with ID: {subscription_id} inserted/updated in database.")
    except Exception as e:
        logging.error(f"Database insertion/update failed: {e}")
        raise

# Liste des statuts acceptés
valid_statuses = ['succeeded', 'paid', 'pending', 'failed', 'canceled', 'requires_payment_method', 'requires_confirmation', 'requires_action', 'processing', 'requires_capture']

def update_subscription_status(subscription_id, status):
    try:
                
        # Vérifier si le statut est valide, sinon, le forcer à 'draft'
        if status not in valid_statuses:
            logging.error(f"Received invalid status: {status} for subscription {subscription_id}. Setting to 'draft'.")
            status = 'draft'
        
        response = supabase.table('subscriptions').update({
            'status': status,
            'updated_at': datetime.utcnow().isoformat()
        }).eq('subscription_id', subscription_id).execute()

        if not response.data:
            raise Exception(f"Failed to update subscription status: {response}")

        logging.info(f"Subscription with ID: {subscription_id} status updated to {status}.")
    except Exception as e:
        logging.error(f"Failed to update subscription status: {e}")
        raise



def upsert_subscription(subscription_id, email, customer_id, price_id, status):
    
    # Valider le statut avant insertion
    if status not in valid_statuses:
        logging.error(f"Invalid status '{status}' received for subscription {subscription_id}. Defaulting to 'draft'.")
        status = 'draft'

    max_tokens = get_plan_tokens(price_id)
    data = {
        "subscription_id": subscription_id,
        "email": email,
        "customer_id": customer_id,
        "price_id": price_id,
        "status": status,
        'total_tokens_used': 0,
        'max_tokens': max_tokens,
        'created_at': datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }

    try:
        response = supabase.table('subscriptions').upsert(data, on_conflict=['email']).execute()

        if not response.data:
            raise Exception(f"Failed to insert/update data: {response}")

        logging.info(f"Subscription with ID: {data.get('subscription_id')} inserted/updated in database.")
    except Exception as e:
        logging.error(f"Database insertion/update failed: {e}")
        return "Database error", 500

    
    
        
@app.route('/api/check-payment-status', methods=['GET'])
def check_payment_status():
    email = request.args.get('email')
    if not email:
        return jsonify({"message": "Email is required"}), 400

    try:
        subscription = supabase.table('subscriptions').select('status').eq('email', email).execute()
        if subscription.data:
            status = subscription.data[0].get('status')
            if status in ('succeeded', 'paid'):
                return jsonify({"hasPaid": True}), 200
        return jsonify({"hasPaid": False}), 200
    except Exception as e:
        logging.error(f"Error checking payment status for {email}: {e}")
        return jsonify({"message": str(e)}), 500

# ----------------------------------------------------------------


# ------------------------- webhook --------------------------------





@app.route('/api/webhook', methods=['POST'])
def webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('Stripe-Signature')
    endpoint_secret = os.getenv('STRIPE_ENDPOINT_SECRET')

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)

        email = None
        customer_id = None
        price_id = None
        status = None
        subscription_id = None

        event_type = event['type']

        if event_type == "customer.subscription.deleted":
            subscription = event['data']['object']
            subscription_id = subscription.get('id')
            status = "canceled"
            update_subscription_status(subscription_id, status)

        elif event_type == "customer.subscription.updated":
            subscription = event['data']['object']
            subscription_id = subscription.get('id')
            status = subscription.get('status')

            # Valider le statut reçu avant de l'envoyer à la mise à jour
            valid_statuses = ['active', 'trialing', 'past_due', 'incomplete', 'incomplete_expired', 'canceled']
            if status not in valid_statuses:
                logging.error(f"Invalid status '{status}' received from Stripe. Defaulting to 'draft'.")
                status = 'draft'
            
            update_subscription_status(subscription_id, status)




        if event_type.startswith("invoice.") or event_type.startswith("customer.subscription."):
            invoice = event['data']['object']

            if isinstance(invoice, stripe.api_resources.abstract.APIResource):
                invoice = dict(invoice)

            subscription_id = invoice.get('subscription')
            customer_id = invoice.get('customer')
            email = invoice.get('customer_email') or stripe.Customer.retrieve(customer_id).get('email')

            if not email and customer_id:
                # Requête Stripe pour obtenir l'email si non inclus dans l'événement
                customer = stripe.Customer.retrieve(customer_id)
                email = customer.get('email')
            
            # Parcourir les lignes de facturation pour récupérer l'ID du prix
            price_id = None

            for line in invoice.get('lines', {}).get('data', []):
                if 'price' in line:
                    price_id = line['price']['id']
                    break
            
            # Récupérer le statut de la facture
            status = invoice.get('status')
            upsert_subscription(subscription_id, email, customer_id, price_id, status)

            # if subscription_id:
            #     upsert_subscription(subscription_id, email, customer_id, price_id, status)


        return '', 200
    except Exception as e:
        logging.error(f"Webhook error: {e}")
        return "Webhook error", 400
    


if __name__ == '__main__':
    app.run(debug=True)
    port = int(os.getenv("PORT", 5000))
    if port == 5000:
        app.run(debug=True)
    else:
        app.run(host='0.0.0.0', port=port, debug=False)