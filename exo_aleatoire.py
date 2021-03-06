from random import randrange

def exo_aleatoire() -> str : 
    """ 
    Fonctionnalité BETA visant à générer sur demande un exercice aléatoire issu des TDs
    et à l'afficher, formaté en LaTeX, pour l'utilisateur l'ayant demandé
    """
    latex = open("fichiers/tex/TD25.tex")

    texte = latex.read()
    exos = texte.split("\\nex")[1:-1]

    latex.close()

    ex = exos[randrange(len(exos))]
    while ex[-1]== '\\' or ex[-1] == "  ":
        ex.pop(-1)

    ex.replace("associe", "longmapsto")
    ex.replace("\\R", "\\mathbb{R}")
    ex.replace("\\N", "\\mathbb{N}")
    ex.replace("\\Q", "\\mathbb{Q}")

    return ex