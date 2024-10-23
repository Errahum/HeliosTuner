import os
import time
import stripe
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
# Configurez vos clés API
stripe.api_key = os.getenv("stripe_key_test_backend")
supabase_url: str  = os.getenv("SUPABASE_URL")
supabase_key: str  = os.getenv("SUPABASE_SERVICE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

def create_product_and_price():
    # Créer un produit
    product = stripe.Product.create(name="Test Product", description="Produit pour tests")

    # Créer un prix avec un intervalle de 1 mois (remplacez par un autre intervalle si nécessaire)
    price = stripe.Price.create(
        unit_amount=1000,  # Montant en cents (10,00 $)
        currency="usd",
        recurring={"interval": "month"},  # Utilisez un intervalle valide
        product=product.id,
    )

    return product.id, price.id

def create_customer():
    # Créer un client de test
    customer = stripe.Customer.create(
        email="test@example.com",
        name="Test Customer"
    )
    return customer.id

def create_subscription(customer_id, price_id):
    subscription = stripe.Subscription.create(
        customer=customer_id,
        items=[{"price": price_id}],
        trial_end=int(time.time()) + 60  # Une minute de période d'essai
    )

    return subscription.id

def cancel_subscription_after_delay(subscription_id):
    time.sleep(65)  # Attendre 65 secondes pour s'assurer que la période d'essai est terminée
    stripe.Subscription.delete(subscription_id)

def update_supabase(subscription_id, status):
    data = {
        "subscription_id": subscription_id,
        "status": status,
        "updated_at": time.strftime('%Y-%m-%d %H:%M:%S')
    }
    response = supabase.table("subscriptions").update(data).eq("subscription_id", subscription_id).execute()
    return response

def verify_cancellation(subscription_id):
    subscription = stripe.Subscription.retrieve(subscription_id)
    return subscription.status == "canceled"

if __name__ == "__main__":
    # Créer un produit et un prix
    product_id, price_id = create_product_and_price()
    print(f"Produit créé avec ID : {product_id}")
    print(f"Prix créé avec ID : {price_id}")

    # Créer un client de test
    customer_id = create_customer()
    print(f"Client créé avec ID : {customer_id}")

    # Créer un abonnement pour le client de test
    subscription_id = create_subscription(customer_id, price_id)
    print(f"Abonnement créé avec ID : {subscription_id}")

    # Annuler l'abonnement après le délai
    cancel_subscription_after_delay(subscription_id)
    print(f"Abonnement {subscription_id} annulé")

    # Mettre à jour la base de données Supabase
    update_response = update_supabase(subscription_id, "canceled")
    print(f"Réponse de mise à jour Supabase : {update_response}")

    # Vérifier l'annulation
    if verify_cancellation(subscription_id):
        print(f"Abonnement {subscription_id} annulé et vérifié avec succès")
    else:
        print(f"Échec de la vérification de l'annulation pour l'abonnement {subscription_id}")
        