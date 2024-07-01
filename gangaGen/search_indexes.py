# your_app_name/search_indexes.py

from haystack import indexes
from .models import Proteins

class ProteinsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    metadata_accession = indexes.CharField(model_attr='metadata_accession')
    name = indexes.CharField(model_attr='name')
    source_database = indexes.CharField(model_attr='source_database')
    length = indexes.IntegerField(model_attr='length')
    source_organism_taxId = indexes.CharField(model_attr='source_organism_taxId')
    source_organism_scientificName = indexes.CharField(model_attr='source_organism_scientificName')
    source_organism_fullName = indexes.CharField(model_attr='source_organism_fullName')
    gene = indexes.CharField(model_attr='gene', null=True)
    in_alphafold = indexes.BooleanField(model_attr='in_alphafold')
    entries_accession = indexes.CharField(model_attr='entries_accession')
    start = indexes.IntegerField(model_attr='start')
    end = indexes.IntegerField(model_attr='end')
    dc_status = indexes.CharField(model_attr='dc_status')
    representative = indexes.BooleanField(model_attr='representative')
    model = indexes.CharField(model_attr='model')
    score = indexes.FloatField(model_attr='score')
    protein_length = indexes.IntegerField(model_attr='protein_length')
    entry_source_database = indexes.CharField(model_attr='entry_source_database')
    entry_type = indexes.CharField(model_attr='entry_type')
    entry_integrated = indexes.CharField(model_attr='entry_integrated')
    sequence = indexes.CharField(model_attr='sequence')

    def get_model(self):
        return Proteins

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
