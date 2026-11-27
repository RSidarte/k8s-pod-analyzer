import requests
import os

from outils import compter_par

from dotenv import load_dotenv
load_dotenv()                          # lit le fichier .env
token = os.environ.get("GITHUB_TOKEN")



def infos_github(utilisateur):
    url = f"https://api.github.com/users/{utilisateur}/repos"
    headers = {"Authorization": f"Bearer {token}"}
   
    reponse = requests.get(url, headers=headers, timeout=10)
    print("Code HTTP :", reponse.status_code)
    print("Limite :", reponse.headers.get("X-RateLimit-Limit"))
    print("Token absent :", token is None)
    print("Longueur :", len(token) if token else 0)
    print("Début :", token[:11] if token else None)
    if reponse.status_code == 404:
        print("❌ Utilisateur introuvable")
        return []
    if reponse.status_code != 200:
        print(f"❌ Erreur {reponse.status_code}")
        return []

    donnees = reponse.json()
    repos = []
    for repo in donnees:
        langage = repo["language"] or "Inconnu"
        repos.append(
            {
                "nom": repo["name"],
                "langage": langage,
                "etoiles": repo["stargazers_count"],
            }
        )
    return repos


repos = infos_github("rsidarte")
print(compter_par(repos, "langage"))
