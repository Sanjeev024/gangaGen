# your_app_name/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):
    access_code = models.CharField(max_length=50, unique=True, blank=True, null=True)

    # Specify unique related_name for groups and user_permissions
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set', blank=True)

    def __str__(self):
        return self.username


class Protein(models.Model):
    id = models.CharField(max_length=255, primary_key=True)  # Assuming Id is a string
    name = models.CharField(max_length=255)
    organism = models.CharField(max_length=255)
    domain = models.CharField(max_length=255)

    def __str__(self):
        return self.name  # Display name in admin panel or wherever object is displayed
    

class Proteins(models.Model):
    metadata_accession = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    source_database = models.CharField(max_length=50)
    length = models.IntegerField()
    source_organism_taxId = models.CharField(max_length=50)
    source_organism_scientificName = models.CharField(max_length=255)
    source_organism_fullName = models.CharField(max_length=255)
    gene = models.CharField(max_length=100, null=True)
    in_alphafold = models.BooleanField()
    entries_accession = models.CharField(max_length=50)
    start = models.IntegerField()
    end = models.IntegerField()
    dc_status = models.CharField(max_length=20)
    representative = models.BooleanField()
    model = models.CharField(max_length=50)
    score = models.FloatField()
    protein_length = models.IntegerField()
    entry_source_database = models.CharField(max_length=50)
    entry_type = models.CharField(max_length=50)
    entry_integrated = models.CharField(max_length=50)
    sequence = models.TextField()

    def __str__(self):
        return self.name