import requests

from outils import compter_par


def infos_github(utilisateur):
    url = f"https://api.github.com/users/{utilisateur}/repos"
    reponse = requests.get(url, timeout=10)
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
