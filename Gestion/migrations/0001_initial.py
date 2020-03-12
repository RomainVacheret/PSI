# Generated by Django 3.0.3 on 2020-03-08 07:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Composante',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(max_length=50)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('date_MAJ', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Formation',
            fields=[
                ('id_formation', models.AutoField(primary_key=True, serialize=False)),
                ('VET', models.IntegerField()),
                ('libelle', models.CharField(max_length=50)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('date_MAJ', models.DateTimeField(auto_now=True)),
                ('composantes', models.ManyToManyField(to='Gestion.Composante')),
            ],
            options={
                'unique_together': {('id_formation', 'VET')},
            },
        ),
        migrations.CreateModel(
            name='Individu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50)),
                ('prenom', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('numero', models.CharField(max_length=8, unique=True)),
                ('telephone', models.CharField(max_length=10)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('date_MAJ', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Modalite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(max_length=50)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('date_MAJ', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Niveau',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(max_length=50)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('date_MAJ', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Salle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batiment', models.CharField(max_length=15)),
                ('numero', models.IntegerField()),
                ('capacite', models.IntegerField()),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('date_MAJ', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Type_individu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(max_length=50)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('date_MAJ', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Type_seance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(max_length=50)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('date_MAJ', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Seance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_debut', models.TimeField()),
                ('date_fin', models.TimeField()),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('date_MAJ', models.DateTimeField(auto_now=True)),
                ('fid_individu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Gestion.Individu')),
                ('fid_salle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Gestion.Salle')),
                ('fid_type_seance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Gestion.Type_seance')),
            ],
        ),
        migrations.AddField(
            model_name='individu',
            name='fid_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Gestion.Type_individu'),
        ),
        migrations.CreateModel(
            name='Groupe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(max_length=50)),
                ('annee', models.CharField(max_length=4)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('date_MAJ', models.DateTimeField(auto_now=True)),
                ('etudiants', models.ManyToManyField(to='Gestion.Individu')),
                ('fid_formation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Gestion.Formation')),
                ('fid_modalite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Gestion.Modalite')),
                ('fid_niveau', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Gestion.Niveau')),
            ],
        ),
    ]
