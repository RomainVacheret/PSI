from django.db import models


class Type_individu(models.Model):
    libelle = models.CharField(max_length=50)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_MAJ = models.DateTimeField(auto_now=True)


class Individu(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    numero = models.CharField(max_length=8, unique=True)
    telephone = models.CharField(max_length=10)  
    fid_type = models.ForeignKey(Type_individu, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_MAJ = models.DateTimeField(auto_now=True)


class Composante(models.Model):
    libelle = models.CharField(max_length=50)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_MAJ = models.DateTimeField(auto_now=True)


class Niveau(models.Model):
    libelle = models.CharField(max_length=50)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_MAJ = models.DateTimeField(auto_now=True)


class Formation(models.Model):
    id_formation = models.AutoField(primary_key=True)
    VET = models.IntegerField()  
    libelle = models.CharField(max_length=50)
    composantes = models.ManyToManyField(Composante)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_MAJ = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('id_formation', 'VET')


class Modalite(models.Model):
    libelle = models.CharField(max_length=50)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_MAJ = models.DateTimeField(auto_now=True)


class Salle(models.Model):
    batiment = models.CharField(max_length=15)
    numero = models.IntegerField()
    capacite = models.IntegerField()
    date_creation = models.DateTimeField(auto_now_add=True)
    date_MAJ = models.DateTimeField(auto_now=True)


class Groupe(models.Model):
    libelle = models.CharField(max_length=50)  
    annee = models.CharField(max_length=4) 
    fid_niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE)
    fid_formation = models.ForeignKey(Formation, on_delete=models.CASCADE)
    fid_modalite = models.ForeignKey(Modalite, on_delete=models.CASCADE)
    etudiants = models.ManyToManyField(Individu)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_MAJ = models.DateTimeField(auto_now=True)


class Type_seance(models.Model):
    libelle = models.CharField(max_length=50)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_MAJ = models.DateTimeField(auto_now=True)


class Seance(models.Model):
    date_debut = models.TimeField()
    date_fin = models.TimeField()
    fid_type_seance = models.ForeignKey(Type_seance, on_delete=models.CASCADE)
    fid_individu = models.ForeignKey(Individu, on_delete=models.CASCADE)  
    fid_salle = models.ForeignKey(Salle, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_MAJ = models.DateTimeField(auto_now=True)


