import json


def create_jsonl_entry(system_role, user_role, assistant_role):
    entry = {
        "messages": [
            {"role": "system", "content": system_role},
            {"role": "user", "content": user_role},
            {"role": "assistant", "content": assistant_role}
        ]
    }
    return entry


def save_to_jsonl(filename, entry):
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    print(f"Entrée sauvegardée dans {filename}.")
