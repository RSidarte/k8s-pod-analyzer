def compter_par(elements, cle):
    compteur = {}
    for element in elements:
        valeur = element[cle]
        if valeur in compteur:
            compteur[valeur] += 1
        else:
            compteur[valeur] = 1
    return compteur