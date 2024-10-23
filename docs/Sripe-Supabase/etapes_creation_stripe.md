### 3. Créer une route backend pour générer la session de paiement (via Stripe)

Dans ton backend Flask, tu devras créer une route qui gère la création de la session de paiement Stripe. Voici un exemple avec Flask :

import stripe
from flask import Flask, request, jsonify

app = Flask(__name__)

stripe.api_key = 'sk_test_XXXXXXXXXXXXXXXXXXXX'

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    data = request.get_json()
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': data['priceId'],
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url='https://your-website.com/success',
            cancel_url='https://your-website.com/cancel',
        )
        return jsonify({'id': session.id})
    except Exception as e:
        return jsonify(error=str(e)), 403

Cette route crée une session de paiement et renvoie l'ID de session à ton frontend.

### 4. Gérer le webhook Stripe pour valider l'abonnement

Après un paiement réussi, tu devras écouter les **webhooks Stripe** pour savoir si l'abonnement est actif. Stripe enverra des événements comme `invoice.payment_succeeded` que tu peux utiliser pour activer l'accès au produit numérique dans Supabase.

Voici un exemple de webhook dans Flask :

@app.route('/webhook', methods=['POST'])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('Stripe-Signature')
    endpoint_secret = 'whsec_XXXXXXXXXXXXXXXXXXXX'
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return jsonify(success=False), 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return jsonify(success=False), 400

    # Handle the event
    if event['type'] == 'invoice.payment_succeeded':
        session = event['data']['object']
        # Accorder l'accès au produit numérique dans Supabase ici
        user_id = session['customer']
        # Logique pour activer l'accès dans Supabase

    return jsonify(success=True)

### 5. Accorder l'accès au produit numérique via Supabase

Une fois que tu reçois un webhook Stripe confirmant que le paiement est réussi, tu peux mettre à jour ton utilisateur dans Supabase (par exemple, avec un champ `is_subscribed` ou une table `subscriptions`).

Cela peut se faire en utilisant l'API de Supabase pour marquer cet utilisateur comme ayant un accès actif au produit numérique.

import supabase

# Initialise le client Supabase
supabase_client = supabase.create_client('https://your-supabase-url', 'public-anon-key')

def grant_access_to_user(user_id):
    supabase_client.from_('users').update({'is_subscribed': True}).eq('id', user_id).execute()

### 6. Vérifier l'accès dans le frontend

À chaque fois que l'utilisateur accède à son compte, tu vérifies via Supabase s'il a un abonnement actif et donc accès au produit numérique.
