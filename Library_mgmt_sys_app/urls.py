from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

app_name = 'Library_mgmt_sys_app'
urlpatterns = [
    path('authors/', csrf_exempt(views.AuthorsView.as_view())),
    path('languages/', csrf_exempt(views.LanguagesView.as_view())),
    path('publishers/', csrf_exempt(views.PublishersView.as_view())),
    path('books/', csrf_exempt(views.BooksView.as_view())),
    path('users/', csrf_exempt(views.UsersView.as_view())),
    path('ebooks/', csrf_exempt(views.EbooksView.as_view())),
    path('hardcopys/', csrf_exempt(views.HardCopysView.as_view())),
    path('search/', csrf_exempt(views.SearchView.as_view()))
]
