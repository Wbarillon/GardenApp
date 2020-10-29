"""Sensorialys_django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from Sensorialys_django_app import views

'''
Compréhension de path :
1er argument est l'url affichée
2e argument est le nom de la vue dans views.py
3e argument est le nom de l'url dans un template. Pour passer des variables dans un template, il faut que ces variables soient disponibles dans celui-ci. Puis, il faut les indiquer dans l'url du template comme ceci :

{% url 'name' <variable 1> <variable 2> %}
Exemple :
{% url 'actualiser_lot' culture_name_data datum.id %}
'''

webpages_patterns = [
    path('', views.index, name = 'index'),
    path('etat_jardin', views.etat_jardin, name = 'etat_jardin'),
    path('etat_jardin/<str:nom_culture>/', views.etat_jardin_detail, name = 'etat_jardin_detail'),
    path('ressources_jardin', views.ressources_jardin, name = 'ressources_jardin')
]

forms_patterns = [
    path('etat_jardin/ajout_culture', views.ajout_culture, name = 'ajout_culture'),
    path('etat_jardin/<str:nom_culture>/ajout_lot', views.ajout_lot, name = 'ajout_lot'),
    path('ressources_jardin/ajout_graine', views.ajout_graine, name = 'ajout_graine'),
    path('etat_jardin/actualiser_culture/<str:nom_culture>', views.actualiser_culture, name = 'actualiser_culture'),
    path('etat_jardin/<str:nom_culture>/actualiser_lot/<int:id>', views.actualiser_lot, name = 'actualiser_lot'),
    path('ressources_jardin/actualiser_graine/<int:id>', views.actualiser_graine, name = 'actualiser_graine')
]

github_patterns = [
    path("update_server/", views.update, name="update")
]

urlpatterns = [
    path('', include(webpages_patterns)),
    path('', include(forms_patterns)),
    path('', include(github_patterns))
]