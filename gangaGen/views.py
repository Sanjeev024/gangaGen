from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator
import requests
from .models import Proteins
from django.http import JsonResponse
from haystack.query import SearchQuerySet
import logging
import re

# Define a logger instance
logger = logging.getLogger(__name__)



from .models import CustomUser

def home(request):
    return render(request, 'index.html')

def user_login(request):
    if request.method == 'POST':
        access_code = request.POST.get('access_code')
        user = authenticate(request, access_code=access_code)
        if user is not None:
            login(request, user)
            masked_access_code = ' '.join(list('⬤' * (len(access_code) - 2) + access_code[-2:]))
            request.session['access_code'] = masked_access_code  # Store access code in session
            return redirect('database')
        else:
            messages.error(request, "Wrong Credentials")
    return redirect('home')

def logout_view(request):
    logout(request)
    return redirect('home')

def database(request):
    if not request.user.is_authenticated:
        messages.error(request, "You are not logged in.")
        return redirect('home')

    # Retrieve access code from session
    masked_access_code = request.session.get('access_code', '')

    # Get the page number from the request, defaulting to 1
    page_number = request.GET.get('page', 1)
    
    # Calculate the batch number based on the page number
    batch_number = (int(page_number) - 1) // 1000 + 1

    # Calculate the starting index based on the batch number
    start_index = (batch_number - 1) * 1000

    # Calculate the ending index
    end_index = start_index + 1000

    # Fetch data from the Protein table within the specified range
    protein_data = Proteins.objects.all()[start_index:end_index]

    # Pagination
    paginator = Paginator(protein_data, 10)  # Show 10 records per page
    page_obj = paginator.get_page(page_number)
    print(page_obj.paginator.page_range)
    print(page_obj.number)
    


    # Retrieve unique organism names from the Protein model
    organism_names = Proteins.objects.values_list('source_organism_fullName', flat=True).distinct()
    entries_accession = Proteins.objects.values_list('source_organism_fullName', flat=True).distinct()
    start = Proteins.objects.values_list('start', flat=True).distinct()
    end = Proteins.objects.values_list('start', flat=True).distinct()
     # Create a set to collect unique combinations
    # Fetch distinct combinations of organism, entry accession, start, and end values
    # Create domain_names by combining all distinct values
    domain_names = []
    for protein in protein_data:
        domain_name = f"{protein.source_organism_fullName}-{protein.entries_accession} ({protein.start}-{protein.end})"
        domain_names.append(domain_name)

    context = {
        'organism_names': organism_names
    }

    return render(request, 'database.html', {'access_code': masked_access_code, 'page_obj': page_obj,  'organism_names': organism_names, 'domains_names': domain_names})

def search_proteins(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'})

    # Get the search query parameters from the request
    name = request.GET.get('name', '')
    organism = request.GET.get('organism', '')
    domain = request.GET.get('domain', '')

    # Extract entries_accession, start, and end from the domain string
    domain_pattern = re.compile(r'-([A-Z0-9]+) \((\d+)-(\d+)\)')
    match = domain_pattern.search(domain)
    if match:
        entries_accession = match.group(1)
        start = match.group(2)
        end = match.group(3)
    else:
        return JsonResponse({'error': 'Invalid domain format'}, status=400)

    # Construct the Solr query URL with the provided parameters
    solr_url = f'http://localhost:8983/solr/protiensSearch/select?q=name%3A%22{name}%22%20AND%20source_organism_fullName%3A%22{organism}%22%20AND%20entries_accession%3A%22{entries_accession}%22%20AND%20start%3A%22{start}%22%20AND%20end%3A%22{end}%22&indent=true&rows=1&useParams='


    try:
        # Make a GET request to the Solr endpoint
        response = requests.get(solr_url)
        # Check if the request was successful
        if response.status_code == 200:
            #Return the Solr response directly
            print(response.json())
            return JsonResponse(response.json())
        else:
            # If the request was not successful, return an error response
            return JsonResponse({'error': 'Failed to fetch search results from Solr'}, status=500)
    except Exception as e:
        # If an exception occurs during the request, return an error response
        return JsonResponse({'error': str(e)}, status=500)
    
def search_sequence(request):
    if not request.user.is_authenticated:
        messages.error(request, "You are not logged in.")
        return redirect('home')

    # Retrieve access code from session
    masked_access_code = request.session.get('access_code', '')

    # Get the page number from the request, defaulting to 1
    page_number = request.GET.get('page', 1)
    
    # Calculate the batch number based on the page number
    batch_number = (int(page_number) - 1) // 1000 + 1

    # Calculate the starting index based on the batch number
    start_index = (batch_number - 1) * 1000

    # Calculate the ending index
    end_index = start_index + 1000

    # Fetch data from the Protein table within the specified range
    protein_data = Proteins.objects.all()[start_index:end_index]

    # Pagination
    paginator = Paginator(protein_data, 10)  # Show 10 records per page
    page_obj = paginator.get_page(page_number)
    print(page_obj.paginator.page_range)
    print(page_obj.number)
    


    # Retrieve unique organism names from the Protein model
    organism_names = Proteins.objects.values_list('source_organism_fullName', flat=True).distinct()
    entries_accession = Proteins.objects.values_list('source_organism_fullName', flat=True).distinct()
    start = Proteins.objects.values_list('start', flat=True).distinct()
    end = Proteins.objects.values_list('start', flat=True).distinct()
     # Create a set to collect unique combinations
    # Fetch distinct combinations of organism, entry accession, start, and end values
    # Create domain_names by combining all distinct values
    domain_names = []
    for protein in protein_data:
        domain_name = f"{protein.source_organism_fullName}-{protein.entries_accession} ({protein.start}-{protein.end})"
        domain_names.append(domain_name)

    context = {
        'organism_names': organism_names
    }

    return render(request, 'search_sequence.html', {'access_code': masked_access_code, 'page_obj': page_obj,  'organism_names': organism_names, 'domains_names': domain_names})
def search_seq(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'})

    # Get the search query parameters from the request
    sequence = request.GET.get('sequence', '')
   

    

    # Construct the Solr query URL with the provided parameters
    solr_url = f'http://localhost:8983/solr/protiensSearch/select?q=sequence%3A%22{sequence}%22&indent=true&rows=1&useParams='


    try:
        # Make a GET request to the Solr endpoint
        response = requests.get(solr_url)
        # Check if the request was successful
        if response.status_code == 200:
            #Return the Solr response directly
            print(response.json())
            return JsonResponse(response.json())
        else:
            # If the request was not successful, return an error response
            return JsonResponse({'error': 'Failed to fetch search results from Solr'}, status=500)
    except Exception as e:
        # If an exception occurs during the request, return an error response
        return JsonResponse({'error': str(e)}, status=500)