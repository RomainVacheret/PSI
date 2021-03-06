from django.contrib import admin
from django.urls import path, include
from . import views as Gestion_views

urlpatterns = [
    path('', Gestion_views.accueil, name='accueil_gestion'),
    path('import', Gestion_views.import_fichier, name='import_gestion'),
    path('export', Gestion_views.export_fichier, name='export_gestion'),
    path('composantes', Gestion_views.affichage_composantes, name='affichage_composantes_gestion'),
    path('niveaux', Gestion_views.affichage_niveaux, name='affichage_niveaux_gestion'),
    path('modalites', Gestion_views.affichage_modalites, name='affichage_modalites_gestion'),
    path('salles', Gestion_views.affichage_salles, name='affichage_salles_gestion'),

    path('individu/recherche', Gestion_views.recherche_individu, name='recherche_individu_gestion'),
    path('individu/ajout', Gestion_views.ajout_individu, name='ajout_individu_gestion'),
    path('individu/<numero>', Gestion_views.affichage_individu, name='affichage_individu_gestion'),
    path('individu/<numero>/modification', Gestion_views.modification_individu, name='modification_individu_gestion'),
    path('individu/<numero>/suppression', Gestion_views.suppression_individu, name='suppression_individu_gestion'),

    path('promotion/recherche', Gestion_views.recherche_promotion, name='recherche_promotion_gestion'),
    path('promotion/ajout', Gestion_views.ajout_promotion, name='ajout_promotion_gestion'),
    path('promotion/<libelle>', Gestion_views.affichage_promotion, name='affichage_promotion_gestion'),
    path('promotion/<libelle>/suppression', Gestion_views.suppression_promotion, name='suppression_promotion_gestion'),
    path('promotion/<libelle>/inscription', Gestion_views.inscription_etudiant, name='inscription_gestion'),
    path('promotion/<libelle>/desinscription/<numero>', Gestion_views.desinscription_etudiant, name='desinscription_gestion'),
    
    path('seance/recherche', Gestion_views.recherche_seance, name='recherche_seance_gestion'),
    path('seance/ajout', Gestion_views.ajout_seance, name='ajout_seance_gestion'),
    path('seance/<pk>', Gestion_views.affichage_seance, name='affichage_seance_gestion'),
    path('seance/<pk>/suppression', Gestion_views.suppression_seance, name='suppression_seance_gestion'),
    path('seance/<pk>/modification', Gestion_views.modification_seance, name='modification_seance_gestion'),

    


]
