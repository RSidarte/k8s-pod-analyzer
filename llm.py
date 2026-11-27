import json
from analyse import parser_json, pods_en_erreur, pods_instables
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

SYSTEME = (
    "Tu es un expert SRE Kubernetes. "
    "Pour chaque pod, donne la cause probable et les commandes kubectl à lancer. "
    "Sois concis."
)


def construire_description(pods):
    lignes = []
    noms_a_verifier = pods_en_erreur(pods) + pods_instables(pods)
    for pod in pods:
        if pod["nom"] in noms_a_verifier:
            lignes.append(
                f"{pod['nom']} : statut {pod['statut']}, restarts: {pod['restarts']}, namespace: {pod['namespace']}"
            )
    return "\n".join(lignes)


def diagnostiquer(pods):
    description = construire_description(pods)
    if not description:
        return "✅ Aucun pod à diagnostiquer"
    message = client.messages.create(
        model="claude-haiku-5-5",
        max_tokens=300,
        system=SYSTEME,
        messages=[
            {"role": "user", "content": f"Voici les pods à problème :\n{description}"}
        ],
    )
    textes = []
    for bloc in message.content:
        if bloc.type == "text":
            textes.append(bloc.text)
    if message.stop_reason == "max_tokens":
        textes.append("⚠️ Réponse tronquée")
    return "\n".join(textes)


if __name__ == "__main__":
    with open("pods.json") as fichier:
        datas = json.load(fichier)

    pods = parser_json(datas)
    print(diagnostiquer(pods))
