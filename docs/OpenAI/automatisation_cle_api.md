
# Automatisation de la génération de clés d'API lors d'un achat avec Stripe et OpenAI

Il semble que tu as une base solide avec ton système actuel, en intégrant Stripe, Supabase, et JWT pour les abonnements et l'authentification. Pour aller plus loin et répondre à la question de la génération automatique de clés d'API lors des achats, voici un plan pour gérer cela en utilisant Stripe et OpenAI :

## 1. Étape de validation de l'achat (via Stripe)

Après qu'un utilisateur ait effectué un achat, tu peux écouter l'événement `checkout.session.completed` envoyé par Stripe. Cela te permet de vérifier que le paiement a bien été effectué avant de générer la clé d'API. Utilise un webhook Stripe comme tu l'as déjà configuré pour écouter ces événements.

## 2. Génération automatique d'une clé d'API

Une fois que tu as validé l'achat (par exemple via l'événement Stripe), tu peux utiliser l'API d'OpenAI pour générer une clé d'API (token d'accès) pour cet utilisateur. Assure-toi que l'utilisateur a un compte lié à OpenAI dans ton organisation.

Pour générer cette clé via OpenAI, voici un exemple de requête Python :

```python
import openai

openai.organization = "org-id"
openai.api_key = "clé-maître"

# Crée un jeton d'accès API pour l'utilisateur
api_key = openai.ApiKey.create(
    owner="utilisateur@example.com",
    scope="user"
)

# Stocke la clé dans la base de données
store_api_key_in_db(user_email, api_key)
```

## 3. Stockage sécurisé de la clé d'API

Une fois générée, tu devrais stocker cette clé de manière sécurisée dans ta base de données. Assure-toi de ne pas la stocker en clair. Tu pourrais chiffrer la clé avant de la stocker dans la colonne dédiée à l'API de ton utilisateur dans Supabase. Par exemple, tu peux utiliser la bibliothèque `cryptography` pour cela.

```python
from cryptography.fernet import Fernet

# Génère une clé de chiffrement sécurisée (à stocker de manière sécurisée)
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Chiffre la clé API
encrypted_api_key = cipher_suite.encrypt(api_key.encode())

# Stocke l'API chiffrée dans la base de données
store_encrypted_api_key_in_db(user_email, encrypted_api_key)
```

## 4. Colonnes supplémentaires dans la base de données

Comme tu envisages d'ajouter des colonnes pour `total_tokens_used` et `last_used_at`, voici comment tu pourrais modifier la structure de ta table Supabase `subscriptions` :

```sql
ALTER TABLE subscriptions
ADD COLUMN total_tokens_used integer DEFAULT 0,
ADD COLUMN last_used_at timestamp;
```

Ensuite, chaque fois que l'utilisateur utilise des tokens via l'API, tu peux mettre à jour ces valeurs dans la base de données.

## 5. Mise à jour des tokens utilisés

À chaque appel API, tu peux compter les tokens utilisés et mettre à jour la colonne `total_tokens_used`. Par exemple :

```python
def update_token_usage(user_email, tokens_used):
    # Récupère les informations d'abonnement actuelles
    subscription = get_subscription_by_email(user_email)
    
    # Incrémente le nombre de tokens utilisés
    new_total = subscription['total_tokens_used'] + tokens_used

    # Met à jour dans la base de données
    update_total_tokens_used(user_email, new_total)
```

## Conclusion

Avec ce système, tu pourrais automatiser la génération de clés d'API après un achat, suivre l'utilisation des tokens, et mettre à jour les informations d'abonnement et d'utilisation dans Supabase de manière efficace.
