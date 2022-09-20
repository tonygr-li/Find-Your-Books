from django.urls import path
from . import views
from .views import EditPost, PostDeleteView

urlpatterns = [
    path('', views.home_en, name='sell-home'), #Home page du site web

    path('sell/', views.CreatePost, name='sell'), #Création post pour vendre quelque chose
    path('want/', views.WantCreatePost, name='want'), #Création post où on veut quelque chose

    path('ad/<int:pk>', views.PostInfo, name='post-info'), #Page quand on clique sur post
    path('ad/edit-add-img/<int:pk>', views.UpdatePostAddImages, name='update-post-img'), #Edit images du post
    path('ad/edit/<int:pk>', EditPost.as_view(), name='update-post'), #Edit post
    path('ad/delete/<int:pk>', PostDeleteView.as_view(), name='delete-post'), #Supprimer post
    path('ad/author/<int:pk>', views.PostAuthorProfile, name='post-author'),

    path('search/', views.Search, name='search'), #Par défaut: post les plus récents en premier
    path('search-by-price-low/', views.PriceLowSearch, name='low-price-search'), #Prix plus bas à plus haut
    path('search-by-price-high/', views.PriceHighSearch, name='high-price-search'), #Prix haut à bas
    path('search-by-date-old/', views.DateOldSearch, name='search-old'), #Moins récents en premier
    path('search-offer/', views.SearchOffer, name='search-offer'), #Only offered results show
    path('search-wanted/', views.SearchWant, name='search-want'),
]