import os
import json
import django

# Set up Django's settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()
from django.db.models import Count, F
from gangaGen.models import Proteins

# Assuming you want to find duplicates based on name, source organism full name, and sequence
duplicate_entries = Proteins.objects.values('name', 'source_organism_fullName', 'sequence').annotate(count=Count('id')).filter(count__gt=1)

# Iterate through duplicate entries
for entry in duplicate_entries:
    duplicates = Proteins.objects.filter(name=entry['name'], source_organism_fullName=entry['source_organism_fullName'], sequence=entry['sequence'])

    # Check for differences in entries_accession, start, and end
    for duplicate in duplicates:
        other_duplicates = duplicates.exclude(id=duplicate.id)
        for other_duplicate in other_duplicates:
            if duplicate.entries_accession != other_duplicate.entries_accession or \
                duplicate.start != other_duplicate.start or \
                duplicate.end != other_duplicate.end:
                print(f"Entries {duplicate.metadata_accession} and {other_duplicate.metadata_accession} have same name, source organism full name, and sequence but different entries_accession, start, or end.")
