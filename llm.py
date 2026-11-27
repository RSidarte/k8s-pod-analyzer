import json, sys, anthropic, subprocess
from analyse import parser_json, pods_en_erreur, pods_instables
from dotenv import load_dotenv


load_dotenv()
client = anthropic.Anthropic()

SYSTEME = (
    "Tu es un expert SRE Kubernetes. "
    "Pour chaque pod, donne la cause probable et les commandes kubectl à lancer. "
    "Sois concis."
)


def recuperer_pods(namespace):
    resultat = subprocess.run(
        ["kubectl", "get", "pods", "-n", namespace, "-o", "json"],
        capture_output=True,
        text=True,
    )
    if resultat.returncode != 0:
        print(f"❌ Erreur kubectl : {resultat.stderr}")
        return None
    return json.loads(resultat.stdout)


def construire_description(pods):
    lignes = []
    noms_a_verifier = pods_en_erreur(pods) + pods_instables(pods)
    for pod in pods:
        if pod["nom"] in noms_a_verifier:
            ligne = (
                f"{pod['nom']} : statut {pod['statut']}, "
                f"restarts: {pod['restarts']}, namespace: {pod['namespace']}"
            )
            if pod["derniere_erreur"]:
                ligne += f", dernière erreur: {pod['derniere_erreur']}, code sortie: {pod['code_sortie']}"
            lignes.append(ligne)
    return "\n".join(lignes)


def diagnostiquer(pods):
    description = construire_description(pods)
    if not description:
        return "✅ Aucun pod à diagnostiquer"
    message = client.messages.create(
        model="claude-haiku-5-5",
        max_tokens=2000,
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
    datas = recuperer_pods("demo")
    if datas is None:
        sys.exit(1)
    pods = parser_json(datas)
    print(diagnostiquer(pods))
   
