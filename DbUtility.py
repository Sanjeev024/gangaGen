import os
import json
import django

# Set up Django's settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

# Now you can import your model using relative import
from gangaGen.models import Proteins

def populate_database():
    with open('output_PF00704.json') as f:
        data = json.load(f)  # Load the entire JSON file
        for item in data:
            metadata = item['metadata']
            extra_fields = item['extra_fields']
            entries = item['entries'][0]  # Assuming there's only one entry for simplicity

            # Create or update Protein instance
            protein, created = Proteins.objects.update_or_create(
                metadata_accession=metadata['accession'],
                defaults={
                    'name': metadata['name'],
                    'source_database': metadata['source_database'],
                    'length': metadata['length'],
                    'source_organism_taxId': metadata['source_organism']['taxId'],
                    'source_organism_scientificName': metadata['source_organism']['scientificName'],
                    'source_organism_fullName': metadata['source_organism']['fullName'],
                    'gene': metadata['gene'],
                    'in_alphafold': metadata['in_alphafold'],
                    'entries_accession': entries['accession'],
                    'start': entries['entry_protein_locations'][0]['fragments'][0]['start'],
                    'end': entries['entry_protein_locations'][0]['fragments'][0]['end'],
                    'dc_status': entries['entry_protein_locations'][0]['fragments'][0]['dc-status'],
                    'representative': entries['entry_protein_locations'][0]['fragments'][0]['representative'],
                    'model': entries['entry_protein_locations'][0]['model'],
                    'score': entries['entry_protein_locations'][0]['score'],
                    'protein_length': entries['protein_length'],
                    'entry_source_database': entries['source_database'],
                    'entry_type': entries['entry_type'],
                    'entry_integrated': entries['entry_integrated'],
                    'sequence': extra_fields['sequence']
                }
            )

if __name__ == '__main__':
    populate_database()
