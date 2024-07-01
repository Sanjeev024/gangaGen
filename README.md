# GangaGen-django-project
A simple app built with django


### Setup -[Ubuntu]
Update the System
```bash
sudo apt-get update
```
To get this repository, run the following command inside your git enabled terminal
```bash
git clone [copy link from clone]
```
You will need django to be installed in you computer to run this app. Head over to https://www.djangoproject.com/download/ for the download guide

Download django usig pip
```bash
sudo apt install python3-pip -y
```
```bash
pip install django
```
Once you have downloaded django, go to the cloned repo directory and run the following command

```bash
python3 manage.py makemigrations
```

This will create all the migrations file (database migrations) required to run this App.

Now, to apply this migrations run the following command
```bash
python3 manage.py migrate
```

One last step and then our  App will be live. We need to create an admin user to run this App. On the terminal, type the following command and provide username, password and email for the admin user
```bash
python3 manage.py createsuperuser
```

That was pretty simple, right? Now let's make the App live. We just need to start the server now and then we can start using our simple App. Start the server by following command

```bash
python3 manage.py runserver
```

Once the server is hosted, head over to http://127.0.0.1:8000/ for the App.

# Integrating Solr with Django Project

This guide provides step-by-step instructions for setting up Apache Solr with a Django project using `django-haystack`.

## Step 1: Install and Set Up Solr

1. **Download Solr**:
   - Download the latest version of Solr from the [Apache Solr Downloads page](https://lucene.apache.org/solr/downloads.html).

2. **Install Solr**:
   - Extract the downloaded archive and navigate to the Solr directory. Start the Solr server:
     ```bash
     bin/solr start
     ```

3. **Create a Core**:
   - Create a new core for your Django project. A core in Solr is a running instance that uses its own configuration.
     ```bash
     bin/solr create -c mycore
     ```

## Step 2: Install and Configure `django-haystack`

1. **Install `django-haystack` and `pysolr`**:
   - Install the necessary packages using pip:
     ```bash
     pip install django-haystack pysolr
     ```

2. **Add `django-haystack` to Your Installed Apps**:
   - Add `haystack` to the `INSTALLED_APPS` list in your Django `settings.py`:
     ```python
     INSTALLED_APPS = [
         ...
         'haystack',
     ]
     ```

3. **Configure Haystack in Django Settings**:
   - Configure Haystack to use the Solr backend in your `settings.py`:
     ```python
     HAYSTACK_CONNECTIONS = {
         'default': {
             'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
             'URL': 'http://127.0.0.1:8983/solr/mycore',
         },
     }
     ```

## Step 3: Create Search Indexes

1. **Create a Search Index for Your Models**:
   - Create a file named `search_indexes.py` in the app where your models are defined. Define search indexes for the models you want to index:
     ```python
     # myapp/search_indexes.py

     from haystack import indexes
     from .models import MyModel

     class MyModelIndex(indexes.SearchIndex, indexes.Indexable):
         text = indexes.CharField(document=True, use_template=True)

         def get_model(self):
             return MyModel

         def index_queryset(self, using=None):
             return self.get_model().objects.all()
     ```

2. **Create a Search Index Template**:
   - Create a template for the search index fields in a directory named `templates/search/indexes/myapp/mymodel_text.txt`:
     ```html
     {{ object.field1 }}
     {{ object.field2 }}
     ```

## Step 4: Rebuild the Search Index

1. **Run the `rebuild_index` Command**:
   - Rebuild the search index to populate it with the data from your models:
     ```bash
     python manage.py rebuild_index
     ```

## Step 5: Implement Search Functionality in Django

1. **Create a Search Form**:
   - Create a search form to handle search queries from users:
     ```python
     # myapp/forms.py

     from django import forms
     from haystack.forms import SearchForm

     class MySearchForm(SearchForm):
         def no_query_found(self):
             return self.searchqueryset.all()
     ```

2. **Create a Search View**:
   - Create a view to handle search requests and render search results:
     ```python
     # myapp/views.py

     from haystack.query import SearchQuerySet
     from django.shortcuts import render
     from .forms import MySearchForm

     def search_view(request):
         form = MySearchForm(request.GET or None)
         results = form.search() if form.is_valid() else SearchQuerySet().all()
         return render(request, 'search/search.html', {'form': form, 'results': results})
     ```

3. **Create a Search Template**:
   - Create a template to display the search form and search results:
     ```html
     <!-- templates/search/search.html -->

     <form method="get" action=".">
         {{ form.as_p }}
         <input type="submit" value="Search">
     </form>

     <ul>
         {% for result in results %}
             <li>{{ result.object }}</li>
         {% endfor %}
     </ul>
     ```

4. **Add a URL Pattern for the Search View**:
   - Add a URL pattern to route search requests to the search view:
     ```python
     # myapp/urls.py

     from django.urls import path
     from .views import search_view

     urlpatterns = [
         ...
         path('search/', search_view, name='search'),
     ]
     ```

By following these steps, you should be able to configure Solr with your Django project, index your models, and implement search functionality using `django-haystack`.


Cheers and Happy Coding :)
