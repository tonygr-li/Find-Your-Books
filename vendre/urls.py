from django.urls import path
from . import views
from .views import EditPost, PostDeleteView

urlpatterns = [
    path('', views.home_en, name='sell-home-fr'), #Home page du site web

    path('vendre/', views.CreatePost, name='sell-fr'), #Création post pour vendre quelque chose
    path('vouloir/', views.WantCreatePost, name='want-fr'), #Création post où on veut quelque chose

    path('publication/<int:pk>', views.PostInfo, name='post-info-fr'), #Page quand on clique sur post
    path('publication/mettre-a-jour-images/<int:pk>', views.UpdatePostAddImages, name='update-post-img-fr'), #Edit images du post
    path('publication/mettre-a-jour/<int:pk>', EditPost.as_view(), name='update-post-fr'), #Edit post
    path('publication/effacer/<int:pk>', PostDeleteView.as_view(), name='delete-post-fr'), #Supprimer post
    path('publication/auteur/<int:pk>', views.PostAuthorProfile, name='post-author-fr'),

    path('chercher/', views.Search, name='search-fr'), #Par défaut: post les plus récents en premier
    path('chercher-par-prix-bas/', views.PriceLowSearch, name='low-price-search-fr'), #Prix plus bas à plus haut
    path('chercher-par-prix-haut/', views.PriceHighSearch, name='high-price-search-fr'), #Prix haut à bas
    path('chercher-par-date-vieux/', views.DateOldSearch, name='search-old-fr'), #Moins récents en premier
    path('chercher-offre/', views.SearchOffer, name='search-offer-fr'), #Only offered results show
    path('chercher-vouloir/', views.SearchWant, name='search-want-fr'),
]