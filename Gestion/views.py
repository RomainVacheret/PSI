from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from django.contrib import messages
from . import utilitaire
from .models import (
    Individu,
    Composante,
    Niveau,
    Formation,
    Modalite,
    Salle,
    Groupe,
    Seance,
    Type_individu,
)
from .forms import (
    Form_recherche_individu,
    Form_ajout_individu,
    Form_modification_individu,
    Form_recherche_promotion,
    Form_ajout_promotion,
    Form_import_fichier,
)
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView, 
    DeleteView,
)



clefs_individu = ('nom', 'prenom', 'numero', 'email', 'telephone')

def accueil(requete):
    return render(requete, 'Gestion/accueil.html')

def import_fichier(requete):
    contexte = {
        'titre': 'Import fichier',
        'formulaire': Form_import_fichier()
    }

    if requete.method == 'POST':
        formulaire = Form_import_fichier(requete.POST, requete.FILES)
        if formulaire.is_valid():
            fichier = requete.FILES['fichier']
            if not fichier.name.endswith('.csv'):
                messages.warning(requete, 'le fichier n\'est pas un csv !')

            else:
                donnees = fichier.read().decode('UTF-8')
                erreurs, total = utilitaire.traitement_fichier(donnees)
                if total == erreurs:
                    messages.warning(requete, 'Echec de l\'import !\n')

                else:
                    messages.success(requete, f'Import effectue ! {erreurs} erreur(s)\n')
                    return redirect('accueil_gestion')
                
        else:
            messages.warning(requete, 'Erreur lors de l\'import !\n')
    
    return render(requete, 'Gestion/import_fichier.html', contexte)
                
def export_fichier(requete):
    pass       


def affichage_generique(requete, liste_donnees, nom_element):
    contexte = {
        'informations': liste_donnees,
        'titre': f'Liste {nom_element}',
        'nom_element': nom_element.capitalize()
    }
    return render(requete, 'Gestion/affichage.html', contexte)


def affichage_composantes(requete):
    liste = [{'Libelle': composante.libelle} for composante in Composante.objects.all()]

    return affichage_generique(requete, liste, 'composantes')


def affichage_niveaux(requete):
    liste = [{'Libelle': niveau.libelle} for niveau in Niveau.objects.all()]

    return affichage_generique(requete, liste, 'niveaux')


def affichage_modalites(requete):
    liste = [{'Libelle': modalite.libelle} for modalite in Modalite.objects.all()]

    return affichage_generique(requete, liste, 'modalites')


# def recherche_individu(requete):
#     contexte = {
#         'titre': 'Recherche individu',
#         'formulaire': Form_recherche_individu(),
#         'nom_element': 'individus',
#         'affichage': False,
#         'url_modification': 'modification_individu_gestion'
#     }

#     if requete.method == 'POST':
#         formulaire = Form_recherche_individu(requete.POST)
        
#         if formulaire.is_valid():
#             donnees = formulaire.cleaned_data
#             liste_elements = ('prenom', 'nom', 'email', 'numero', 'telephone', 'fid_type')
#             liste_individus = Individu.objects.values(*liste_elements)
#             liste_attributs = ('fid_type_id', 'numero', 'nom')
            
#             if donnees['type_individu'] == 'Choix':
#                 donnees['type_individu'] = ''

#             for clef, valeur in zip(liste_attributs, donnees.values()):
#                 if valeur:
#                     liste_individus = liste_individus.filter(**{clef:valeur})
           
#             liste_individus = [{
#                 (clef.capitalize() if clef != 'fid_type' else 'Type'): \
#                     (valeur if clef != 'fid_type' \
#                     else Type_individu.objects.get(pk=valeur).libelle) 
#                 for clef, valeur in individu.items()} for individu in liste_individus]

#             contexte.update({
#                 'affichage': True,
#                 'informations': liste_individus,
#             })

#     return render(requete, 'Gestion/recherche.html', contexte)


def ajout_individu(requete):
    contexte = {
        'titre': 'Ajout individu',
        'formulaire': Form_ajout_individu(),
        'nom_element': 'individus',
    }

    liste_elements = ('prenom', 'nom', 'email', 'numero', 'telephone', 'fid_type')

    if requete.method == 'POST':
        formulaire = Form_ajout_individu(requete.POST)

        if formulaire.is_valid():
            verification_unique = (individu.numero for individu in Individu.objects.all())
            donnees = formulaire.cleaned_data

            if donnees.get('numero') not in verification_unique:         
                individu = Individu(**donnees)
                individu.save(donnees)
                messages.success(requete, f'Individu {donnees.get("prenom")} {donnees.get("nom")} cree !')
                return redirect('accueil_gestion')
            else:
                messages.warning(requete, 'Ce numero est deja attribue !')
                contexte.update({'formulaire': Form_ajout_individu(donnees)})
            
    return render(requete, 'Gestion/ajout.html', contexte)


def modification_individu(requete):
    contexte = {
        'titre': 'Modification individu',
        'formulaire':  Form_modification_individu(),
        'nom_element': 'individus'
    }

    liste_elements = ('prenom', 'nom', 'email', 'numero', 'telephone', 'fid_type')

    if requete.method == 'POST':
        if 'modification' in requete.POST:
            print('toto')
            donnees = {clef: valeur for clef, valeur in requete.POST.dict().items() if clef in liste_elements}
            formulaire = Form_modification_individu(donnees)
            formulaire.nom = donnees['nom']
            formulaire.fid_type_id = ()
            contexte.update({'formulaire': formulaire})
        
        elif 'validation' in requete.POST:
            print('titi')
            formulaire = Form_modification_individu(requete.POST)
        
            if formulaire.is_valid():
                donnees = formulaire.cleaned_data
                Individu.objects.get(numero=donnees['numero']).update(**donnees)
                messages.success(requete, f'Individu {donnees.get("prenom")} {donnees.get("nom")} modifie !')
                return redirect('accueil_gestion')
        else:
            raise Exception('Erreur -- modification_individu')
            
    return render(requete, 'Gestion/ajout.html', contexte)


# def recherche_promotion(requete):
#     contexte = {
#         'titre': 'Recherche promotion',
#         'formulaire': Form_recherche_promotion(),
#         'nom_element': 'promotions',
#         'affichage': False,
#         'url_modification': 'modification_promotion_gestion'
#     }

#     if requete.method == 'POST':
#         formulaire = Form_recherche_promotion(requete.POST)
        
#         if formulaire.is_valid():
#             donnees = formulaire.cleaned_data
#             liste_elements = ('annee', 'fid_formation_id', 'fid_modalite_id', 'fid_niveau_id', 'libelle')
#             liste_promotions = Groupe.objects.values(*liste_elements)
            
#             for element in liste_elements[1:-1]:
#                 if donnees[element] == 'Choix':
#                     donnees[element] = ''

#             for clef, valeur in zip(liste_elements, donnees.values()):
#                 if valeur:
#                     liste_promotions = liste_promotions.filter(**{clef:valeur})
            
#             def valeur_fonction_classe(attribut, valeur):
#                 assert attribut in (liste_elements[1:])
#                 if attribut == 'fid_formation_id':
#                     return Formation.objects.get(pk=valeur).libelle

#                 elif attribut == 'fid_modalite_id':
#                     return Modalite.objects.get(pk=valeur).libelle

#                 else:
#                     return Niveau.objects.get(pk=valeur).libelle

#             liste_promotions = [{
#                 'slug': promotion['libelle'],
#                 'instance': {(clef.capitalize() if 'fid' not in clef else clef.split('_')[1].capitalize()): \
#                     (valeur_fonction_classe(clef, valeur) if 'fid' in clef else valeur)
#                 for clef, valeur in promotion.items() if clef != 'libelle'}} for promotion in liste_promotions]
                        
#             contexte.update({
#                 'affichage': True,
#                 'informations': liste_promotions,
#             })

#     return render(requete, 'Gestion/recherche.html', contexte)


def recherche_promotion(requete):
    contexte = {
        'titre': 'Recherche promotion',
        'formulaire': Form_recherche_promotion(),
        'nom_element': 'promotions',
        'affichage': False,
        'url_modification': 'modification_promotion_gestion'
    }

    if requete.method == 'POST':
        formulaire = Form_recherche_promotion(requete.POST)
        
        if formulaire.is_valid():
            donnees = formulaire.cleaned_data
            liste_elements = ('annee', 'fid_formation_id', 'fid_modalite_id', 'fid_niveau_id', 'libelle')
            liste_promotions = Groupe.objects.values('libelle')
            
            for element in liste_elements[1:-1]:
                if donnees[element] == 'Choix':
                    donnees[element] = ''

            for clef, valeur in zip(liste_elements, donnees.values()):
                if valeur:
                    liste_promotions = liste_promotions.filter(**{clef:valeur})
            
            def valeur_fonction_classe(attribut, valeur):
                assert attribut in (liste_elements[1:])
                if attribut == 'fid_formation_id':
                    return Formation.objects.get(pk=valeur).libelle

                elif attribut == 'fid_modalite_id':
                    return Modalite.objects.get(pk=valeur).libelle

                else:
                    return Niveau.objects.get(pk=valeur).libelle

            # liste_promotions = [{
            #     'slug': promotion['libelle'],
            #     'instance': {(clef.capitalize() if 'fid' not in clef else clef.split('_')[1].capitalize()): \
            #         (valeur_fonction_classe(clef, valeur) if 'fid' in clef else valeur)
            #     for clef, valeur in promotion.items() if clef != 'libelle'}} for promotion in liste_promotions]

            liste_promotions = [{
                'slug': promotion['libelle'],
                'instance': {'libelle': promotion['libelle']}
            } for promotion in liste_promotions]

            print(liste_promotions)
                        
            contexte.update({
                'url_name': 'affichage_promotion_gestion',
                'affichage': True,
                'informations': liste_promotions,
            })

    return render(requete, 'Gestion/recherche.html', contexte)


def ajout_promotion(requete):
    contexte = {
        'titre': 'Ajout individu',
        'formulaire': Form_ajout_promotion(),
        'nom_element': 'individus',
    }

    liste_elements = ('annee', 'fid_niveau_id', 'fid_modalite_id', 'fid_formation_id')

    if requete.method == 'POST':
        formulaire = Form_ajout_promotion(requete.POST)

        if formulaire.is_valid():
            donnees = formulaire.cleaned_data

            formations = {str(formation.id_formation): formation.libelle for formation in Formation.objects.all()}
            modalites = {str(modalite.id): modalite.libelle for modalite in Modalite.objects.all()}
            niveaux = {str(niveau.id): niveau.libelle for niveau in Niveau.objects.all()}
            
            libelle = '{} {} {} {}'.format(
                donnees["annee"],
                niveaux[donnees["fid_niveau_id"]],
                modalites[donnees["fid_modalite_id"]],
                formations[donnees["fid_formation_id"]]
            )

            donnees['libelle'] = libelle
            promotion = Groupe(**donnees)

            verification = Groupe.objects.all()
            
            for clef, valeur in zip(liste_elements, donnees.values()):
                if valeur:
                    verification = verification.filter(**{clef:valeur})

            if verification.count():
                messages.warning(requete, 'Cette promotion exite deja !')
                contexte.update({'formulaire': Form_ajout_promotion(donnees)})
            else:        
                promotion.save()
                messages.success(requete, f'Promotion {donnees["libelle"]} creee !')
                return redirect('accueil_gestion')
                
            
    return render(requete, 'Gestion/ajout.html', contexte)


def modification_promotion(requete):
    pass


class Suppression_individu(DeleteView):
    model = Individu
    template_name = 'Gestion/suppression.html'
    success_url = '/'


def recherche_individu(requete):
    contexte = {
        'titre': 'Recherche individu',
        'formulaire': Form_recherche_individu(),
        'nom_element': 'individus',
        'affichage': False,
        'url_modification': 'modification_individu_gestion'
    }

    if requete.method == 'POST':
        formulaire = Form_recherche_individu(requete.POST)
        
        if formulaire.is_valid():
            donnees = formulaire.cleaned_data
            liste_elements = ('prenom', 'nom', 'numero', 'fid_type')
            liste_individus = Individu.objects.values(*liste_elements)
            liste_attributs = ('fid_type_id', 'numero', 'nom')
            
            if donnees['type_individu'] == 'Choix':
                donnees['type_individu'] = ''

            for clef, valeur in zip(liste_attributs, donnees.values()):
                if valeur:
                    liste_individus = liste_individus.filter(**{clef:valeur})

            liste_tmp = []
            for individu in liste_individus:
                liste_tmp.append({
                    'slug': individu['numero'],
                    'instance': {(clef.capitalize() if clef != 'fid_type' else 'Type'): \
                        (valeur if clef != 'fid_type' \
                        else Type_individu.objects.get(pk=valeur).libelle) 
                    for clef, valeur in individu.items()}
                })
           
            # liste_individus = [{
            #         'slug':'individu',
            #         'instance': {(clef.capitalize() if clef != 'fid_type' else 'Type'): \
            #             (valeur if clef != 'fid_type' \
            #             else Type_individu.objects.get(pk=valeur).libelle) 
            #         for clef, valeur in individu.items()}} for individu in liste_individus]

            # for a in liste

            contexte.update({
                'affichage': True,
                'informations': liste_tmp,
                'url_name': 'affichage_individu_gestion',
            })

    return render(requete, 'Gestion/recherche.html', contexte)


def affichage_individu(requete, numero):
    try:
        individu = Individu.objects.filter(numero=numero).values()[0]
    except:
        individu = None
        individu_id = None

    if individu:
        types_invididus = {type_individu.id: type_individu.libelle for type_individu in Type_individu.objects.all()}
        # individu = model_to_dict(individu)
        individu_id = individu.pop('id')
        print('id------', individu_id)
        individu['fid_type_id'] = types_invididus[individu['fid_type_id']]

    contexte = {
        'titre': 'Individu {0}'.format(numero),
        'nom_element': 'individus',
        'element': individu,
        'numero': numero,
        'element_id': individu_id,
    }

    return render(requete, 'Gestion/affichage_detail.html', contexte)


def affichage_promotion(requete, libelle):
    print(f'--{libelle}--')
    for a in Groupe.objects.all():
        print(a, f'--{a.libelle}--')
    try:
        promotion = Groupe.objects.filter(libelle=libelle).values()[0]
    except Exception as e :
        print(e)
        promotion = None
        promotion_id = None

    print(promotion)
    liste_fids = ('fid_formation_id', 'fid_modalite_id', 'fid_niveau_id')
    def valeur_fonction_classe(attribut, valeur):
        assert attribut in liste_fids
        if attribut == 'fid_formation_id':
            return Formation.objects.get(pk=valeur).libelle

        elif attribut == 'fid_modalite_id':
            return Modalite.objects.get(pk=valeur).libelle

        else:
            return Niveau.objects.get(pk=valeur).libelle

    if promotion:
        promotion_id = promotion.pop('id')
        for clef, valeur in promotion.items():
            if 'fid' in clef:
                promotion[clef] = valeur_fonction_classe(clef, valeur)

    print(promotion)

    contexte = {
        'titre': 'Promotion {0}'.format(libelle),
        'nom_element': 'individus',
        'element': promotion,
        'numero': libelle,
        'element_id': promotion_id,
    }

    # if requete.method == 'POST':
    #     formulaire = Form_recherche_promotion(requete.POST)
        
    #     if formulaire.is_valid():
    #         donnees = formulaire.cleaned_data
    #         liste_elements = ('annee', 'fid_formation_id', 'fid_modalite_id', 'fid_niveau_id', 'libelle')
    #         liste_promotions = Groupe.objects.values(*liste_elements)
            
    #         for element in liste_elements[1:-1]:
    #             if donnees[element] == 'Choix':
    #                 donnees[element] = ''

    #         for clef, valeur in zip(liste_elements, donnees.values()):
    #             if valeur:
    #                 liste_promotions = liste_promotions.filter(**{clef:valeur})
            
            

    #         liste_promotions = [{
    #             'slug': promotion['libelle'],
    #             'instance': {(clef.capitalize() if 'fid' not in clef else clef.split('_')[1].capitalize()): \
    #                 (valeur_fonction_classe(clef, valeur) if 'fid' in clef else valeur)
    #             for clef, valeur in promotion.items() if clef != 'libelle'}} for promotion in liste_promotions]
                        
    #         contexte.update({
    #             'affichage': True,
    #             'informations': liste_promotions,
    #         })

    return render(requete, 'Gestion/affichage_detail.html', contexte)