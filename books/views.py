# views.py
from django.views.generic import ListView
from books.models import Publisher, Author
from django.shortcuts import render
from django.http import HttpResponse

class PublisherList(ListView):
	model = Publisher

from django.views.generic.edit import CreateView, UpdateView, DeleteView
class AuthorCreate(CreateView):
	model = Author
	fields = ['name']

from .forms import NameForm
def GetName(request):
	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = NameForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required
			# ...
			# redirect to a new URL:
			FirstName = form.cleaned_data['FirstName']
			LastName = form.cleaned_data['LastName'] 
			return HttpResponse('Get data ok : %s %s' % (FirstName, LastName))

	# if a GET (or any other method) we'll create a blank form
	else:
		form = NameForm() 
		
	return render(request, 'books/name.html', {'form': form})

from .forms import ArticleForm 
from django.forms import formset_factory
def CreateArticleSet(request): 
	ArticleFormSet = formset_factory(ArticleForm, extra = 3)
	formset = ArticleFormSet()
	return render(request, 'books/name.html', {'form': formset})


