from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_personnages, name='liste_personnages'),
    path('personnage/<str:id_personnage>/', views.detail_personnage, name='detail_personnage'),
    path('aide', views.aide, name='aide'),
    path('basculer-cycle/', views.basculer_cycle, name='basculer_cycle'),
]
