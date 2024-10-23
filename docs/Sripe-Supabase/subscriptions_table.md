Configurez la table subscriptions :

Nom de la table : subscriptions
Colonnes :
id: uuid (clé primaire, générée automatiquement)
email: text (pour stocker l'email de l'utilisateur)
customer_id: text (pour stocker l'ID du client Stripe)
subscription_id: text (pour stocker l'ID de l'abonnement Stripe)
price_id: text (pour stocker l'ID du prix)
status: text (pour stocker le statut de l'abonnement, par exemple, "active", "failed")
created_at: timestamp (pour stocker la date de création, optionnel mais recommandé)
updated_at: timestamp (pour stocker la date de mise à jour, optionnel mais recommandé)
total_tokens_used: int4 (stocker les informations concernant l'utilisation des tokens par chaque utilisateur.)
last_used_at: timestamp (Stocke la dernière fois où l'utilisateur a utilisé l'API.)
max_tokens: int (Pour OpenAI, la limite)
moderation: int (Pour voir si l'utilisateur à une probabilité d'être un utilisateur malsain)
Définissez les contraintes :

Vous pouvez définir email, customer_id, subscription_id, et price_id comme non nullables si vous souhaitez vous assurer qu'ils contiennent toujours une valeur.