from import_export.admin import ImportExportModelAdmin
from django.contrib import admin

from .models import *

# Register your models here.

@admin.register(Graine)
class GraineResource(ImportExportModelAdmin):

    list_display = ['id', 'type_graine', 'espece_graine', 'variete_graine', 'niveau_stock', 'provenance', 'annee_recolte', 'remarques', 'nom_usuel']

    list_filter = ['type_graine', 'espece_graine', 'niveau_stock', 'provenance']

@admin.register(Culture)
class CultureResource(ImportExportModelAdmin):

    list_display = ['nom', 'type_contenant']

    list_filter = ['type_contenant']

    search_fields = ['nom']

@admin.register(PhaseCulture)
class RotationCultureResource(ImportExportModelAdmin):

    list_display = ['nom_culture', 'phase', 'phase_date']

@admin.register(EtatLot)
class EtatLotResource(ImportExportModelAdmin):

    list_filter = ['id_lot']

    list_display = ['id', 'id_lot', 'quantite', 'quantite_etat', 'nom_culture', 'etat', 'date', 'phase_lunaire', 'constellation', 'perigee_apogee', 'lunar_node', 'remarques']

@admin.register(Lot)
class LotResource(ImportExportModelAdmin):

    list_display = ['id', 'id_graine', 'nom_culture_initial', 'quantite_lot']



