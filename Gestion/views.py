from django.shortcuts import render, redirect, get_object_or_404
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
    Type_seance,
    Salle
)
from .forms import (
    Form_recherche_individu,
    Form_ajout_individu,
    Form_modification_individu,
    Form_recherche_promotion,
    Form_ajout_promotion,
    Form_import_fichier,
    Form_inscription_etudiants,
    Form_recherche_seance,
    Form_ajout_seance,
    Form_modification_seance
)


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
                return redirect('affichage_individu_gestion', numero=donnees['numero'])
            else:
                messages.warning(requete, 'Ce numero est deja attribue !')
                contexte.update({'formulaire': Form_ajout_individu(donnees)})
            
    return render(requete, 'Gestion/ajout.html', contexte)


def modification_individu(requete, numero):
    contexte = {
        'titre': 'Modification individu',
        'formulaire':  Form_modification_individu(),
        'nom_element': 'individus'
    }

    liste_elements = ('prenom', 'nom', 'email', 'numero', 'telephone', 'fid_type_id')

    if requete.method == 'POST':
        formulaire = Form_modification_individu(requete.POST)

        if formulaire.is_valid():
            donnees = formulaire.cleaned_data
            Individu.objects.filter(numero=donnees['numero']).update(**donnees)
            messages.success(requete, f'Individu {donnees.get("prenom")} {donnees.get("nom")} mis a jour !')
            return redirect('/individu/{}'.format(donnees['numero']))

    instance = Individu.objects.filter(numero=numero).values(*liste_elements)[0]
    formulaire = Form_modification_individu(initial=instance)
    contexte.update({'formulaire': formulaire})
            
    return render(requete, 'Gestion/ajout.html', contexte)


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

            liste_promotions = [{
                'slug': promotion['libelle'],
                'instance': {'libelle': promotion['libelle']}
            } for promotion in liste_promotions]
                        
            contexte.update({
                'nom_url': 'affichage_promotion_gestion',
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
                return redirect('affichage_promotion_gestion', libelle=libelle)
                
            
    return render(requete, 'Gestion/ajout.html', contexte)


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

            liste_individus = [{
                    'slug': individu['numero'],
                    'instance': {(clef.capitalize() if clef != 'fid_type' else 'Type'): \
                        (valeur if clef != 'fid_type' \
                        else Type_individu.objects.get(pk=valeur).libelle) 
                    for clef, valeur in individu.items()}} for individu in liste_individus]


            contexte.update({
                'affichage': True,
                'informations': liste_individus,
                'nom_url': 'affichage_individu_gestion',
            })

    return render(requete, 'Gestion/recherche.html', contexte)


def affichage_individu(requete, numero):
    try:
        individu = Individu.objects.filter(numero=numero).values()[0]
    except Exception as e :
        print(e)
        individu = None
        individu_id = None

    if individu:
        individu_id = individu.pop('id')
        individu['type'] = Type_individu.objects.get(pk=individu.pop('fid_type_id')).libelle
        individu = {clef.capitalize(): valeur for clef, valeur in individu.items()}

    contexte = {
        'titre': 'Individu {0}'.format(numero),
        'nom_element': 'individus',
        'element': individu,
        'erreur': 'Pas d\'individu avec le numero {}'.format(numero),
        'element_id': individu_id,
        'nom_url_modification': 'modification_individu_gestion',
        'slug_modification': numero,
        'slug_suppression': numero,
        'nom_url_suppression': 'suppression_individu_gestion',
        'nom_url_element': 'affichage_promotion_gestion',
        'slug_affichage': 'numero',
        # 'slug_des': True,
        'titre_affichage': 'Liste des promotions de l\'etudiant',
        'liste_affichage': [{'instance': {'Libelle': promotion.libelle}, 'id_': promotion.libelle} for promotion in get_object_or_404(Individu, pk=individu_id).groupe_set.all() if individu['Type'] == 'Eleve'],
    }

    return render(requete, 'Gestion/affichage_detail.html', contexte)


def affichage_promotion(requete, libelle):
    try:
        promotion = Groupe.objects.filter(libelle=libelle).values()[0]
    except Exception as e :
        print(e)
        promotion = None
        promotion_id = None

    def valeur_fonction_classe(attribut, valeur):
        assert attribut in ('fid_formation_id', 'fid_modalite_id', 'fid_niveau_id')
        if attribut == 'fid_formation_id':
            return Formation.objects.get(pk=valeur).libelle

        elif attribut == 'fid_modalite_id':
            return Modalite.objects.get(pk=valeur).libelle

        else:
            return Niveau.objects.get(pk=valeur).libelle

    if promotion:
        promotion_id = promotion.pop('id')
        promotion = {
            (clef.capitalize() if 'fid' not in clef else clef.split('_')[1].capitalize()):
            (valeur if 'fid' not in clef else valeur_fonction_classe(clef, valeur)) 
            for clef, valeur in promotion.items()}

    a = [{'instance': etudiant, 'id_': etudiant['numero']} for etudiant in get_object_or_404(Groupe, pk=promotion_id).etudiants.all().values('numero', 'nom','prenom')],
    print(a)

    contexte = {
        'titre': 'Promotion {0}'.format(libelle),
        'nom_element': 'promotions',
        'element': promotion,
        'erreur': 'Pas de promotion avec le libelle : {}'.format(libelle),
        'element_id': promotion_id,
        'slug_modification': None,
        'slug_suppression': libelle,
        'slug_inscription': libelle,
        'slug_des': True,
        'nom_url_suppression': 'suppression_promotion_gestion',
        'nom_url_element': 'affichage_promotion_gestion',
        'slug_affichage': 'libelle',
        'titre_affichage': 'Liste des etudiants de la promotion',
        'liste_affichage': [{'instance': etudiant, 'id_': etudiant['numero']} for etudiant in get_object_or_404(Groupe, pk=promotion_id).etudiants.all().values('numero', 'nom','prenom')],
    }

    return render(requete, 'Gestion/affichage_detail.html', contexte)

def suppression_promotion(requete, libelle):
    try:
        promotion = get_object_or_404(Groupe, libelle=libelle)
    except Exception as e :
        print(e)
        promotion = None

    if promotion:
        promotion.delete()
        messages.success(requete, 'Promotion {0} supprimee !'.format(libelle))
        return redirect('recherche_promotion_gestion')
    
    messages.warning(requete, 'Erreur lors de la suppression de la promotion {0} !'.format(libelle))
    return redirect('affichage_individu_gestion', libelle=libelle)

    
def suppression_individu(requete, numero):
    try:
        individu = get_object_or_404(Individu, numero=numero)
    except Exception as e :
        print(e)
        individu = None

    if individu:
        individu.delete()
        messages.success(requete, 'Individu {0} supprime !'.format(numero))
        return redirect('recherche_individu_gestion')
    
    messages.warning(requete, 'Erreur lors de la suppression de l\'individu {0} !'.format(numero))
    return redirect('affichage_individu_gestion', numero=numero)


def suppression_seance(requete, pk):
    try:
        seance = get_object_or_404(Seance, id=pk)
    except Exception as e :
        print(e)
        seance = None

    if seance:
        seance.delete()
        messages.success(requete, 'Seance n°{0} supprimee !'.format(pk))
        return redirect('recherche_seance_gestion')
    
    messages.warning(requete, 'Erreur lors de la suppression de la seance n°{0} !'.format(pk))
    return redirect('affichage_seance_gestion', id=pk)


def inscription_etudiant(requete, libelle):
    try:
        promotion = get_object_or_404(Groupe, libelle=libelle)
    except Exception as e :
        print(e)
        messages.warning(requete, 'Erreur lors de l\'inscription dans la promotion {0} !'.format(libelle))
        return redirect('accueil_gestion')

    liste_etudiants = [etudiant.numero for etudiant in promotion.etudiants.all()]

    contexte = {
        'titre': 'Inscription etudiants',
        'formulaire': Form_inscription_etudiants(),
        'libelle': libelle,
        'etudiants': liste_etudiants
    }

    if requete.method == 'POST':
        formulaire = Form_inscription_etudiants(requete.POST)

        if formulaire.is_valid():
            # verification_unique = (individu.numero for individu in Individu.objects.all())
            donnees = formulaire.cleaned_data

            for id_ in donnees['etudiants']:
                etudiant = Individu.objects.get(id=id_)
                promotion.etudiants.add(etudiant)

            messages.success(requete, 'Inscriptions faites avec succes !')
            return redirect('accueil_gestion')

    return render(requete, 'Gestion/inscription.html', contexte)


def desinscription_etudiant(requete, libelle, numero):
    try:
        promotion = get_object_or_404(Groupe, libelle=libelle)
        etudiant = get_object_or_404(Individu, numero=numero)
    except Exception as e :
        print(e)
        promotion = None
        etudiant = None

    if promotion and etudiant:
        promotion.etudiants.remove(etudiant)
        messages.success(requete, 'Desinscriptions de {} dans {} faites avec succes !'.format(numero, libelle))
    else:
        messages.warning(requete, 'Une erreur a eu lieu lors de la desinscriptions ')
    return redirect('accueil_gestion')


def recherche_seance(requete):
    contexte = {
        'titre': 'Recherche seance',
        'formulaire': Form_recherche_seance(),
        'nom_element': 'seances',
        'affichage': False,
        # 'url_modification': 'modification_seance_gestion'
    }

    if requete.method == 'POST':
        formulaire = Form_recherche_seance(requete.POST)
        
        if formulaire.is_valid():
            donnees = formulaire.cleaned_data
            liste_elements = ('id', 'date_debut', 'date_fin', 'fid_type_seance', 'fid_salle', 'fid_individu')
            
            # liste_attributs = ('fid_type_id', 'numero', 'nom')
            

            for element in liste_elements[3:]:
                if donnees[element] == 'Choix':
                    donnees[element] = ''

            liste_seances = Seance.objects.values(*liste_elements)

            for clef, valeur in zip(liste_elements, donnees.values()):
                if valeur:
                    liste_seances = liste_seances.filter(**{clef:valeur})
                    
            # liste_seances = [{
            #         # 'slug': individu['numero'],
            #         'instance': {clef.capitalize(): valeur
            #         for clef, valeur in seance.items()}} for seance in liste_seances]


            liste_tmp = []

            for seance in liste_seances:
                instance = {}
                print(seance.keys())
                for clef, valeur in seance.items():
                    print('-', clef, valeur)
                    if clef in liste_elements[3:]:
                        # print(clef, instance[clef])
                        if clef == 'fid_type_seance':
                            instance['Type'] = Type_seance.objects.get(pk=valeur).libelle
                        elif clef == 'fid_salle':
                            instance['Salle'] = Salle.objects.get(pk=valeur).numero
                        elif clef == 'fid_individu':
                            instance['Enseignant'] = Individu.objects.get(pk=valeur).numero
                    else:
                        instance[clef] = valeur
                for element in liste_elements[2:]:
                    seance.pop(element)
                liste_tmp.append({'instance': instance, 'slug': instance.pop('id')})
                
            
            print(liste_tmp)


            contexte.update({
                'affichage': True,
                'informations': liste_tmp,
                'nom_url': 'affichage_seance_gestion',
            })

    return render(requete, 'Gestion/recherche.html', contexte)


def ajout_seance(requete):
    contexte = {
        'titre': 'Ajout seance',
        'formulaire': Form_ajout_seance(),
        'nom_element': 'seances',
    }

    liste_elements = ('date_debut', 'date_fin', 'fid_type_seance', 'fid_salle', 'fid_individu')

    if requete.method == 'POST':
        formulaire = Form_ajout_seance(requete.POST)

        if formulaire.is_valid():
            donnees = formulaire.cleaned_data

            

            verification = Seance.objects.all()

            for clef, valeur in zip(liste_elements, donnees.values()):
                if valeur:
                    verification = verification.filter(**{clef:valeur})

            if verification.count():
                messages.warning(requete, 'Cette seance exite deja !')
                contexte.update({'formulaire': Form_ajout_promotion(donnees)})
            else:        
                for element in liste_elements[2:]:
                    if element == 'fid_type_seance':
                        donnees[element] = Type_seance.objects.get(pk=donnees[element])
                    elif element == 'fid_salle':
                        donnees[element] = Salle.objects.get(pk=donnees[element])
                    elif element == 'fid_individu':
                        donnees[element] = Individu.objects.get(pk=donnees[element])

                seance = Seance(**donnees)

                seance.save()
                messages.success(requete, 'Seance creee !')
                return render(requete, 'Gestion/accueil.html')
            
    return render(requete, 'Gestion/ajout.html', contexte)



def affichage_seance(requete, pk):
    try:
        seance = Seance.objects.filter(pk=pk).values()[0]
    except Exception as e :
        print(e)
        seance = None
        seance_id = None


    print(seance)

    if seance:
        seance_id = seance.pop('id')
        seance['type'] = Type_seance.objects.get(pk=seance.pop('fid_type_seance_id')).libelle
        seance['professeur'] = Individu.objects.get(pk=seance.pop('fid_individu_id')).numero
        seance['salle'] = Salle.objects.get(pk=seance.pop('fid_salle_id')).numero
        seance = {clef.capitalize(): valeur for clef, valeur in seance.items()}

    contexte = {
        'titre': 'Seance {0}'.format(pk),
        'nom_element': 'seances',
        'element': seance,
        'erreur': 'Pas de seance avec l\'id {}'.format(pk),
        'element_id': pk,
        'nom_url_modification': 'modification_seance_gestion',
        'slug_modification': pk,
        'slug_suppression': pk,
        'nom_url_suppression': 'suppression_seance_gestion',
        'nom_url_element': 'affichage_seance_gestion',
        'slug_affichage': 'numero',
        # 'titre_affichage': 'Liste des promotions de l\'etudiant',
        # 'liste_affichage': [{'Libelle': promotion.libelle} for promotion in get_object_or_404(Individu, pk=individu_id).groupe_set.all() if individu['Type'] == 'Eleve'],
    }

    return render(requete, 'Gestion/affichage_detail.html', contexte)


def modification_seance(requete, pk):
    contexte = {
        'titre': 'Modification seance',
        'formulaire':  Form_modification_seance(),
        'nom_element': 'seances'
    }

    liste_elements = ('id', 'date_debut', 'date_fin', 'fid_type_seance', 'fid_salle', 'fid_individu')

    if requete.method == 'POST':
        formulaire = Form_modification_seance(requete.POST)

        if formulaire.is_valid():
            donnees = formulaire.cleaned_data
            Seance.objects.filter(pk=donnees['id']).update(**donnees)
            messages.success(requete, 'Seance n°{} mise a jour !'.format(pk))
            return redirect('/seance/{}'.format(donnees['id']))

    instance = Seance.objects.filter(pk=pk).values(*liste_elements)[0]
    formulaire = Form_modification_seance(initial=instance)
    contexte.update({'formulaire': formulaire})
            
    return render(requete, 'Gestion/ajout.html', contexte)