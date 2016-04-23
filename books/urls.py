# urls.py
from django.conf.urls import url
from books.views import PublisherList, AuthorCreate, GetName, CreateArticleSet

urlpatterns = [
    url(r'^publishers/$', PublisherList.as_view()),
    url(r'^GetName/$', GetName, name='GetName'),
    url(r'^CreateArticleSet/$', CreateArticleSet, name='CreateArticleSet'),
]
