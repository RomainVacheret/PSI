from django import forms
from .models import (
    Type_individu, 
    Niveau, 
    Modalite, 
    Individu, 
    Formation,
    Salle,
    Type_seance
)

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

    annee = forms.CharField(label='Annee', max_length=4, required=False)
    fid_formation_id = forms.ChoiceField(label='Formation', choices=choix_formations, required=False)
    fid_modalite_id = forms.ChoiceField(label='Modalite', choices=choix_modalites, required=False)
    fid_niveau_id = forms.ChoiceField(label='Niveau', choices=choix_niveaux, required=False)


class Form_ajout_promotion(forms.Form):
    choix_formations = [('', 'Choix')] + [(str(formation.id_formation), formation.libelle) for formation in Formation.objects.all()]
    choix_modalites = [('', 'Choix')] + [(str(modalite.id), modalite.libelle) for modalite in Modalite.objects.all()]
    choix_niveaux = [('', 'Choix')] + [(str(niveau.id), niveau.libelle) for niveau in Niveau.objects.all()]
    
    annee = forms.CharField(label='Annee', max_length=4)
    fid_formation_id = forms.ChoiceField(label='Formation', choices=choix_formations)
    fid_modalite_id = forms.ChoiceField(label='Modalite', choices=choix_modalites)
    fid_niveau_id = forms.ChoiceField(label='Niveau', choices=choix_niveaux)


class Form_import_fichier(forms.Form):
    fichier = forms.FileField()


class Form_inscription_etudiants(forms.Form):
    choix_etudiants = [('', 'Choix')] + [(str(etudiant.id), etudiant.numero) for etudiant in Individu.objects.filter(fid_type=3)]

    etudiants = forms.MultipleChoiceField(label='Etudiants', choices=choix_etudiants)



class Form_recherche_seance(forms.Form):
    choix_professeurs = [('', 'Choix')] + [(professeur.id, professeur.numero) for professeur in Individu.objects.filter(fid_type__in=(1, 2))]
    choix_salles = [('', 'Choix')] + [(salle.id, salle.numero) for salle in Salle.objects.all()]
    choix_seance = [('', 'Choix')] + [(type_.id, type_.libelle) for type_ in Type_seance.objects.all()]

    date_debut = forms.TimeField(label="Date debut", widget=forms.TimeInput(format='%H:%M'), required=False)
    date_fin = forms.TimeField(label="Date fin", widget=forms.TimeInput(format='%H:%M'), required=False)
    fid_individu = forms.ChoiceField(label='Professeur', choices=choix_professeurs, required=False)
    fid_salle = forms.ChoiceField(label='Salle', choices=choix_salles, required=False)
    fid_type_seance = forms.ChoiceField(label='Type', choices=choix_seance, required=False)


class Form_ajout_seance(forms.Form):
    choix_professeurs = [(professeur.id, professeur.numero) for professeur in Individu.objects.filter(fid_type__in=(1, 2))]
    choix_salles = [(salle.id, salle.numero) for salle in Salle.objects.all()]
    choix_seance = [(type_.id, type_.libelle) for type_ in Type_seance.objects.all()]

    date_debut = forms.TimeField(label="Date debut", widget=forms.TimeInput(format='%H:%M'))
    date_fin = forms.TimeField(label="Date fin", widget=forms.TimeInput(format='%H:%M'))
    fid_individu = forms.ChoiceField(label='Professeur', choices=choix_professeurs)
    fid_salle = forms.ChoiceField(label='Salle', choices=choix_salles)
    fid_type_seance = forms.ChoiceField(label='Type', choices=choix_seance)


class Form_modification_seance(forms.Form):
    def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       self.fields['id'].widget.attrs['readonly'] = True

    choix_professeurs = [(professeur.id, professeur.numero) for professeur in Individu.objects.filter(fid_type__in=(1, 2))]
    choix_salles = [(salle.id, salle.numero) for salle in Salle.objects.all()]
    choix_seance = [(type_.id, type_.libelle) for type_ in Type_seance.objects.all()]

    id = forms.IntegerField(label='Numero')
    date_debut = forms.TimeField(label='Date debut', widget=forms.TimeInput(format='%H:%M'), required=True)
    date_fin = forms.TimeField(label='Date fin', widget=forms.TimeInput(format='%H:%M'), required=True)
    fid_individu = forms.ChoiceField(label='Professeur', choices=choix_professeurs, required=True)
    fid_salle = forms.ChoiceField(label='Salle', choices=choix_salles, required=True)
    fid_type_seance = forms.ChoiceField(label='Type', choices=choix_seance, required=True)


