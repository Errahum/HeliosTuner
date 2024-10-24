import stripe
import os

# Configurez votre clé API Stripe
stripe.api_key = os.getenv("stripe_key_backend")

# Vérifiez que la clé API est correctement récupérée
if not stripe.api_key:
    raise ValueError("La clé API Stripe n'est pas définie. Assurez-vous que la variable d'environnement 'stripe_key_test_backend' est correctement définie.")

def get_customer_ids_by_email(email):
    # Récupérer tous les clients avec l'email donné
    customers = stripe.Customer.list(email=email)
    if customers.data:
        return [customer.id for customer in customers.data]
    else:
        raise ValueError(f"Aucun client trouvé avec l'email {email}")

def cancel_all_subscriptions(email):
    try:
        # Obtenir les IDs des clients par email
        customer_ids = get_customer_ids_by_email(email)
        
        for customer_id in customer_ids:
            # Récupérer tous les abonnements du client
            subscriptions = stripe.Subscription.list(customer=customer_id)
            
            # Parcourir chaque abonnement et les annuler
            for subscription in subscriptions.auto_paging_iter():
                canceled_subscription = stripe.Subscription.delete(subscription.id)
                print(f"Abonnement {subscription.id} annulé avec statut : {canceled_subscription.status}")
    except ValueError as e:
        print(e)

# if __name__ == "__main__":
#     # Email du client de test
#     test_customer_email = 
    
#     # Annuler tous les abonnements du client de test
#     try:
#         cancel_all_subscriptions(test_customer_email)
#         print(f"Tous les abonnements du client {test_customer_email} ont été annulés avec succès.")
#     except ValueError as e:
#         print(e)