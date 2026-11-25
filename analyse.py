import sys
import json

from outils import compter_par


def parser(sortie):
    lignes = sortie.splitlines()
    pods = []
    for ligne in lignes[1:]:
        nom, ready, statut, restarts, age = ligne.split()
        pods.append(
            {
                "nom": nom,
                "ready": ready,
                "statut": statut,
                "restarts": int(restarts),
                "namespace": "default",
                "age": age,
            }
        )
    return pods


def parser_json(datas):
    pods = []
    for pod in datas["items"]:
        statuses = pod["status"].get("containerStatuses", [])
        restarts = statuses[0]["restartCount"] if statuses else 0
        pods.append(
            {
                "nom": pod["metadata"]["name"],
                "statut": pod["status"]["phase"],
                "restarts": restarts,
                "namespace": pod["metadata"]["namespace"],
            }
        )
    return pods


def pods_en_erreur(pods):
    list_pods_en_erreur = []
    for pod in pods:
        if pod["statut"] != "Running":
            list_pods_en_erreur.append(pod["nom"])
    return list_pods_en_erreur


def pods_instables(pods):
    instables = []
    for pod in pods:
        if pod["restarts"] > 5:
            instables.append(pod["nom"])
    return instables


def rapport(pods):
    print("=== Rapport du cluster ===")
    if not pods:
        print("Aucun pod dans ce cluster")
        return
    statut_compteur = compter_par(pods, "statut")
    namespace_compteur = compter_par(pods, "namespace")
    erreur_pods = pods_en_erreur(pods)
    print(f"Total : {len(pods)} pods")
    print("=== Par statut ===")
    for statut, nombre in statut_compteur.items():
        print(f"{statut} : {nombre}")
    print("=== Par namespace ===")
    for namespace, nombre in namespace_compteur.items():
        print(f"{namespace} : {nombre}")
    if not erreur_pods:
        print("✅ Aucun pod en erreur")
    else:
        print(f"Pods en erreur : {', '.join(erreur_pods)}")
    instables = pods_instables(pods)
    if not instables:
        print("✅ Aucun pod instable")
    else:
        print(f"Pods instables (> 5 restarts) : {', '.join(instables)}")


try:
    with open("pods.json") as fichier:
        datas = json.load(fichier)
except FileNotFoundError:
    print("❌ Fichier introuvable : pods.json")
    sys.exit(1)

pods = parser_json(datas)
rapport(pods)
