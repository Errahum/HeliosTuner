from heliostuner.src.utils import create_jsonl_entry, save_to_jsonl


def get_input(prompt):
    print(prompt)
    lines = []
    while True:
        line = input()
        if line:
            lines.append(line)
        else:
            break
    return '\n'.join(lines)


def main():
    data = []

    while True:
        print("Entrez les détails pour une nouvelle entrée ou 'exit' pour terminer.")
        system_role = get_input("Entrez le rôle system (ou 'exit' pour terminer) :")
        if system_role.lower() == 'exit':
            break
        user_role = get_input("Entrez le rôle user (ou 'exit' pour terminer) :")
        if user_role.lower() == 'exit':
            break
        assistant_role = get_input("Entrez le rôle assistant (ou 'exit' pour terminer) :")
        if assistant_role.lower() == 'exit':
            break

        entry = create_jsonl_entry(system_role, user_role, assistant_role)

        data.append(entry)

        save_option = input("Voulez-vous sauvegarder l'entrée actuelle dans un fichier? (oui/non) : ").lower()
        if save_option == 'oui':
            filename = input("Entrez le nom du fichier (sans extension) : ") + '.jsonl'
            save_to_jsonl(filename, entry)

    print("Terminé. Toutes les entrées ont été ajoutées.")

#
# if __name__ == "__main__":
#     main()
