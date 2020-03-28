from django import forms
from .models import Type_individu, Niveau, Modalite, Individu, Formation

class Form_recherche_individu(forms.Form):
    choix_types = [('', 'Choix')] + [(str(type_individu.id), type_individu.libelle) for type_individu in Type_individu.objects.all()]
    
    type_individu = forms.ChoiceField(label='Type', choices=choix_types, required=False)
    numero_individu = forms.CharField(label='Numero', max_length=8, required=False)
    nom_individu = forms.CharField(label='Nom', max_length=50, required=False)


class Form_ajout_individu(forms.Form):
    choix_types = [('', 'Choix')] + [(str(type_individu.id), type_individu.libelle) for type_individu in Type_individu.objects.all()]

    nom = forms.CharField(max_length=50, required=False)
    prenom = forms.CharField(max_length=50, required=False)
    numero = forms.CharField(max_length=8, required=False)
    email = forms.CharField(max_length=50, required=False)
    telephone = forms.CharField(max_length=10, required=False)  
    fid_type_id = forms.ChoiceField(label='Type', choices=choix_types, required=False)


class Form_modification_individu(forms.Form):

    def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       self.fields['nom'].widget.attrs['readonly'] = True
       self.fields['numero'].widget.attrs['readonly'] = True
       self.fields['prenom'].widget.attrs['readonly'] = True

    choix_types = [(str(type_individu.id), type_individu.libelle) for type_individu in Type_individu.objects.all()]

    nom = forms.CharField(max_length=50)
    prenom = forms.CharField(max_length=50)
    numero = forms.CharField(max_length=8)
    email = forms.CharField(max_length=50, required=True)
    telephone = forms.CharField(max_length=10, required=True)  
    fid_type_id = forms.ChoiceField(label='Type', choices=choix_types, required=True)


class Form_recherche_promotion(forms.Form):
    choix_formations = [('', 'Choix')] + [(str(formation.id_formation), formation.libelle) for formation in Formation.objects.all()]
    choix_modalites = [('', 'Choix')] + [(str(modalite.id), modalite.libelle) for modalite in Modalite.objects.all()]
    choix_niveaux = [('', 'Choix')] + [(str(niveau.id), niveau.libelle) for niveau in Niveau.objects.all()]
    # choix_etudiants = [(etudiant.id, etudiant.numero) for etudiant in Etudiant.objects.all()]

    annee = forms.CharField(label='Annee', max_length=4, required=False)
    fid_formation_id = forms.ChoiceField(label='Formation', choices=choix_formations, required=False)
    fid_modalite_id = forms.ChoiceField(label='Modalite', choices=choix_modalites, required=False)
    fid_niveau_id = forms.ChoiceField(label='Niveau', choices=choix_niveaux, required=False)
    # etudiants = forms.MultipleChoiceField(label='Etudiant', choices=choix_etudiants, required=False)


class Form_ajout_promotion(forms.Form):
    choix_formations = [('', 'Choix')] + [(str(formation.id_formation), formation.libelle) for formation in Formation.objects.all()]
    choix_modalites = [('', 'Choix')] + [(str(modalite.id), modalite.libelle) for modalite in Modalite.objects.all()]
    choix_niveaux = [('', 'Choix')] + [(str(niveau.id), niveau.libelle) for niveau in Niveau.objects.all()]
    
    annee = forms.CharField(label='Annee', max_length=4)
    fid_formation_id = forms.ChoiceField(label='Formation', choices=choix_formations)
    fid_modalite_id = forms.ChoiceField(label='Modalite', choices=choix_modalites)
    fid_niveau_id = forms.ChoiceField(label='Niveau', choices=choix_niveaux)


# class Form_modification_promotion(forms.Form):
#     choix_formations = [(str(formation.id_formation), formation.libelle) for formation in Formation.objects.all()]
#     choix_modalites = [(str(modalite.id), modalite.libelle) for modalite in Modalite.objects.all()]
#     choix_niveaux = [(str(niveau.id), niveau.libelle) for niveau in Niveau.objects.all()]
    
#     annee = forms.CharField(label='Annee', max_length=4)
#     fid_formation_id = forms.ChoiceField(label='Formation', choices=choix_formations)
#     fid_modalite_id = forms.ChoiceField(label='Modalite', choices=choix_modalites)
#     fid_niveau_id = forms.ChoiceField(label='Niveau', choices=choix_niveaux)


class Form_import_fichier(forms.Form):
    fichier = forms.FileField()
