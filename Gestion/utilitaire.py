import io
import csv
from .models import Individu, Type_individu


def traitement_fichier(donnees):
    cpt = 0
    total = 0
    donnees = io.StringIO(donnees)
    next(donnees)  # si premiere ligne pour les informations

    liste_types = {type_.libelle: type_.id  for type_ in Type_individu.objects.all()}
    attributs = ('nom', 'prenom', 'email', 'numero', 'telephone', 'fid_type_id')
    
    for ligne in csv.reader(donnees, delimiter=','):
        try:
            dict_individu = {clef: (valeur if clef != 'fid_type_id' else liste_types[valeur]) for clef, valeur in zip(attributs, ligne)}
            individu = Individu(**dict_individu)
            individu.save()
        except Exception as e :
            cpt += 1
            print(e)
        total += 1
    
    return cpt, total
