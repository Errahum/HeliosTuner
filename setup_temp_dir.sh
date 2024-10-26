#!/bin/bash

# Chemin du répertoire temporaire
TEMP_DIR=$(pwd)/temp_files

# Créer le répertoire s'il n'existe pas
if [ ! -d "$TEMP_DIR" ]; then
  mkdir -p "$TEMP_DIR"
fi

# Définir les permissions pour le répertoire
# Remplacez 'your_user' par l'utilisateur sous lequel votre application s'exécute
chown -R your_user:your_user "$TEMP_DIR"
chmod -R 700 "$TEMP_DIR"

echo "Le répertoire temporaire a été configuré avec succès."

