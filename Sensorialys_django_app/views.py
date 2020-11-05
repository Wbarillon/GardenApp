from datetime import datetime as dt

from django.shortcuts import render, redirect
from django.db.models import Q
from django.db.models import Count
from django.db.models import Max

# Webhook
import git
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

import os

from .models import *
from .forms import *

# Create your views here.

@csrf_exempt
def update(request):
    if request.method == "POST":
        '''
        pass the path of the diectory where your project will be 
        stored on PythonAnywhere in the git.Repo() as parameter.
        Here the name of my directory is "test.pythonanywhere.com"
        '''
        repo = git.Repo('guiguifsk.eu.pythonanywhere.com/') 
        origin = repo.remotes.origin

        origin.pull()

        return HttpResponse("Updated code on PythonAnywhere")
    else:
        return HttpResponse("Couldn't update the code on PythonAnywhere")


def index(request):
    template_name = 'webpages/index.html'

    # Pour intégrer dans une vue à laquelle on envoie un dictionnaire, il faut que le dictionnaire soit dans un dictionnaire lui-même. Sinon, ça ne marche pas.
    context = {

    }

    return render(request, template_name, context)

def etat_jardin(request):
    template_name = 'webpages/etat_jardin.html'

    context = {

    }

    contenants = Culture.objects.all().values_list('type_contenant', flat = True).distinct().exclude(type_contenant = '')

    if list(contenants):

        phases = Culture.objects.raw("""
            SELECT *, MAX(phase_date)
            FROM Sensorialys_django_app_culture
            LEFT JOIN Sensorialys_django_app_phaseculture
            ON Sensorialys_django_app_phaseculture.nom_culture_id = Sensorialys_django_app_culture.nom
            GROUP BY Sensorialys_django_app_culture.nom
        """)

        fields = ['nom', 'phase']

        labels = []

        for field_name in fields:
            try:
                labels.append(getattr(Culture, field_name).field.verbose_name)
            except AttributeError:
                labels.append(getattr(PhaseCulture, field_name).field.verbose_name)

        context.update({
            'contenants': contenants,
            'phases': phases,
            'labels': labels
        })

    return render(request, template_name, context)

def etat_jardin_detail(request, nom_culture):
    template_name = 'webpages/etat_jardin_detail.html'

    # Valeur obtenue via l'URL dynamique dans urls.py
    culture_name_data = Culture.objects.get(nom = nom_culture)

    context = {
        'culture_name_data': culture_name_data
    }

    fields = ['nom_usuel', 'etat', 'quantite', 'remarques', 'date']

    labels = []

    for field_name in fields:
        try:
            labels.append(getattr(Graine, field_name).field.verbose_name)
        except AttributeError:
            labels.append(getattr(EtatLot, field_name).field.verbose_name)

    '''
    Dans data, nous avons besoin des informations relatives au lot qui sont présentes dans la table graine. Y'a rien à faire pour ça. Pour comprendre le mécanisme, voir "Jointure sur Django ORM" dans "Django le cheat".
    '''

    '''
    Ici, il faut pouvoir afficher même des légumes plantés plus tard qui viennent du même lot parent. En fait on le peut déjà. Il faut :
    - actualiser le lot parent et retirer la quantité à ajouter
    - créer un nouveau lot_parent, même graîne, mêmes infos que le "vrai" lot_parent en ajoutant la quantité
    - et voilà ! Il ne reste plus qu'à créer un lot enfant à partir de ce lot parent
    '''

    '''
    data = EtatLot.objects.raw("""
        SELECT *, MAX(date)
        FROM Sensorialys_django_app_etatlot
        WHERE Sensorialys_django_app_etatlot.nom_culture_id = %s
        GROUP BY Sensorialys_django_app_etatlot.id_lot_id
    """, [nom_culture])
    '''

    '''
    TRÉSOR DE GUERRE : une requête SQL avec une variable
    '''
    '''
    Cette requête doit afficher la dernière entrée enregistrée pour chaque lot présent dans une culture.
    La subtilité vient de l'order by dans le row_number. On classe d'abord par date pour avoir la date la plus récente, puis on classe par id.
    Dans la table temporelle en-dessous, il suffit de sélectionner la première entrée de row_number().
    '''
    data = EtatLot.objects.raw("""
        WITH MyCte AS(
            SELECT *, ROW_NUMBER() OVER(
                PARTITION BY Sensorialys_django_app_etatlot.id_lot_id
                ORDER BY date DESC, Sensorialys_django_app_etatlot.id DESC
            ) AS POSITION
            FROM Sensorialys_django_app_etatlot
            WHERE Sensorialys_django_app_etatlot.nom_culture_id = %s
        ),
        MyCte2 AS(
            SELECT *
            FROM MyCte
            WHERE POSITION = 1
        )
        SELECT *
        FROM MyCte2
    """, [nom_culture])

    if list(data):
        context.update({
            'labels': labels,
            'data': data
        })

    return render(request, template_name, context)

def ressources_jardin(request):
    template_name = 'webpages/ressources_jardin.html'

    fields = ['nom_usuel', 'type_graine', 'niveau_stock', 'provenance', 'annee_recolte', 'remarques']

    context = {
        
    }

    if request.GET.get('search_value') != None:
        search_value = request.GET.get('search_value')
        data = Graine.objects.filter(nom_usuel__contains = search_value)
        context.update({'data': data})
    else:
        data = Graine.objects.all()
        context.update({'data': data})

    labels = []

    for field_name in fields:
        labels.append(getattr(Graine, field_name).field.verbose_name)

    context.update({
        'labels': labels
    })

    return render(request, template_name, context)

# Formulaire simple (trop simple... c'est inutile)
'''
def ajout_culture(request):
    template_name = app_name+'/ajout_culture.html'

    context = {
        
    }

    if request.method == 'POST':
        form = AddCultureStep1(request.POST)
        if form.is_valid():
            post = form.save(commit = False)
            post.save()
    else:
        form = AddCultureStep1()

    context.update({'form_items': form})

    return render(request, template_name, context)
'''

# Formulaires multi-pages

def ajout_lot(request, nom_culture):
    template_name = 'forms/ajout_lot.html'

    form_list = [AddLotStep1, AddLotStep2, AddLotStep3, AddLotStep4]

    models = [Lot, EtatLot]

    fields = ['id_graine', 'quantite', 'remarques', 'etat', 'date', 'phase_lunaire', 'constellation', 'perigee_apogee', 'lunar_node', 'nom_culture']

    form = {
        'step': 1,
        'count': len(form_list)
    }

    form.update({
        'form_fields': form_list[form['step'] -1]
    })

    context = {
        'culture_name_data': nom_culture,
        'form': form
    }

    # Handling GET requests

    if request.GET.get('search_value') != None:
        
        search_value = request.GET.get('search_value')

        if request.session['reponse'] == 'lot_enfant':

            '''
            TRÉSOR DE GUERRE
            Requête de l'orm Django avec des "ou" apporté par Q
            
            search_results_enfant = EtatLot.objects.filter(
                Q(id_lot__id_graine__espece_graine__contains = search_value) |
                Q(id_lot__id_graine__variete_graine__contains = search_value)
            ).filter(etat = 'Germé').exclude(id_lot__quantite_lot = 0)
            '''

            search_results_enfant = EtatLot.objects.filter(id_lot__id_graine__nom_usuel__contains = search_value).filter(etat = 'Germé').exclude(id_lot__quantite_lot = 0)

            context.update({'search_results_enfant': search_results_enfant})

        elif request.session['reponse'] == 'lot_parent':

            search_results_parent = Graine.objects.filter(nom_usuel__contains = search_value)

            context.update({'search_results_parent': search_results_parent})

        form.update({'step': 2})

        context.update({'form': form})

    # Navigation throught steps

    if request.POST.get('next_step') != None:

        for field in fields:
            if request.POST.get(field) != None:
                request.session.update({field: request.POST.get(field)})
            else:
                pass

        data = {key: value for key, value in request.session.items() if key in fields}

        form.update({
            'step': int(request.POST.get('next_step'))
        })

        form.update({
            'form_fields': form_list[form['step'] -1]()
        })

        context.update({'form': form})
    elif request.POST.get('previous_step') != None:
        '''
        Pour stocker les données de l'étape précédente, il suffit de mettre les données dans les "()" du formulaire. Le dictionnaire data peut faire l'affaire.
        '''
        form.update({
            'step': int(request.POST.get('previous_step'))
        })

        form.update({
            'form_fields': form_list[form['step'] -1]()
        })

        context.update({'form': form})

    # step 1

    if request.POST.get('question') != None:
        request.session.update({'reponse': request.POST.get('question')})

    # step 3

    if ('reponse' in dict(request.session.items())) and (request.session['reponse'] == 'lot_enfant') and (form['step'] == 3):

        lot_enfant = EtatLot.objects.get(id = request.session['id_graine'])
        quantite_lot = lot_enfant.id_lot.quantite_lot

        request.session.update({'quantite_lot': quantite_lot})

        context.update({'quantite_lot': quantite_lot})
    
    if (request.POST.get('quantite') != None) and (request.session['reponse'] == 'lot_enfant'):

        quantite_lot = request.session['quantite_lot']

        if request.POST.get('quantite') != '':

            difference = int(quantite_lot) - int(request.session['quantite'])

            if (difference < 0) and (request.POST.get('next_step') != None):

                form_list[form['step'] -1] = AddLotStep3(request.POST or None)

                form.update({
                    'form_fields': form_list[form['step'] -1],
                    'step': 3
                })

                context.update({
                    'form': form,
                    'quantite_lot': quantite_lot,
                    'erreur_quantite': 'erreur_quantite'
                })

    # step 4
    if (request.POST.get('etat') != None) and (len(request.POST) < 6):

        form_list[form['step'] -1] = AddLotStep4(request.POST or None, etat = request.POST.get('etat'))

        form.update({
            'form_fields': form_list[form['step'] -1],
            'step': 4
        })

        context.update({
            'form': form,
            'lunar_calendar': 'lunar_calendar'
        })

    # last step
    elif request.POST.get('confirmation_step') != None:

        for field in fields:
            if request.POST.get(field) != None:
                request.session.update({field: request.POST.get(field)})
            else:
                pass

        # Now, every data from forms have been stored within request.session dictionnary.

        # Transfering data to a dictionnary, becausee it'd be bad practice to process data from request.session.

        data = {key: value for key, value in request.session.items() if key in fields}
        data.update({'nom_culture': nom_culture})

        for key, value in data.items():
            if key == 'id_graine':
                if request.session['reponse'] == 'lot_parent':
                    data.update({key: Graine.objects.get(id = value)})
                elif request.session['reponse'] == 'lot_enfant':
                    lot_enfant = EtatLot.objects.get(id = value)
                    data.update({key: Graine.objects.get(id = lot_enfant.id_lot.id_graine.id)})

        '''
        From data we are going to have :
        - data_front that will display a summary of the form for the user
        - data_back that will save data in the database

        Once the user is satisfied with the summary, he can save data. Otherwise, he starts again from zero.
        '''

        labels = []

        for model in models:
            for field_name in fields:
                try:
                    labels.append(getattr(model, field_name).field.verbose_name)
                except AttributeError:
                    pass

        data_front = {label: value for label, value in zip(labels, data.values())}

        context.update({'data_front': data_front})

    elif request.POST.get('recommencer') != None:

        # Since we restart the form, we better have to clean request.session before
        del request.session['reponse']

        for field in fields:
            try:
                del request.session[field]
            except KeyError:
                pass

        return redirect('ajout_lot', nom_culture = nom_culture)

    elif request.POST.get('sauvegarder') != None:

        data = {key: value for key, value in request.session.items() if key in fields}
        data.update({'nom_culture': nom_culture})

        if data['quantite'] == '':
            data.update({'quantite': None})

        data_back = {}

        for key, value in data.items():
            if key == 'id_graine':
                if request.session['reponse'] == 'lot_parent':
                    data_back.update({key: Graine.objects.get(id = value)})
                elif request.session['reponse'] == 'lot_enfant':
                    lot_enfant = EtatLot.objects.get(id = value)
                    data_back.update({key: Graine.objects.get(id = lot_enfant.id_lot.id_graine.id)})
            elif key == 'nom_culture':
                if request.session['reponse'] == 'lot_parent':
                    data_back.update({
                        key: Culture.objects.get(nom = value),
                        'nom_culture_initial': value
                    })
                elif request.session['reponse'] == 'lot_enfant':
                    data_back.update({
                        key: Culture.objects.get(nom = value)
                    })
            elif key == 'quantite':
                if request.session['reponse'] == 'lot_parent':
                    data_back.update({
                        key: value,
                        'quantite_etat': value,
                        'quantite_lot': value
                    })
                elif request.session['reponse'] == 'lot_enfant':
                    current_quantite = lot_enfant.id_lot.quantite_lot
                    data_back.update({
                        key: value,
                        'quantite_etat': value,
                        'quantite_lot': str(current_quantite - int(value)),
                    })
                    setattr(lot_enfant, key, str(current_quantite - int(value)))
                    lot_enfant.save(update_fields = ['quantite'])
            elif (key.endswith('date')) and (value != ''):
                data_back.update({key: dt.strptime(value, '%d-%m-%Y').strftime('%Y-%m-%d')})
            elif (key.endswith('date')) and (value == ''):
                data_back.update({key: None})
            else:
                data_back.update({key: value})
        
        if request.session['reponse'] == 'lot_parent':
            instance = Lot()

            for key, value in data_back.items():
                setattr(instance, key, value)
            instance.save()

        elif request.session['reponse'] == 'lot_enfant':
            instance = lot_enfant.id_lot

            for key, value in data_back.items():
                setattr(instance, key, value)
            instance.save(update_fields = ['quantite_lot'])

        last_entry = Lot.objects.values('id').last()['id']

        data_back.update({'id_lot': Lot.objects.get(id = last_entry)})

        instance = EtatLot()

        for key, value in data_back.items():
            setattr(instance, key, value)
        instance.save()

        for field in fields:
            try:
                del request.session[field]
            except KeyError:
                pass

        return redirect('etat_jardin_detail', nom_culture = nom_culture)

    return render(request, template_name, context)

def ajout_culture(request):
    template_name = 'forms/one_step_form.html'

    form = AddCulture(request.POST or None, reponse = request.POST.get('question'))

    models = [Culture, PhaseCulture]

    fields = ['type_contenant', 'nom', 'phase', 'phase_date']

    context = {
        'form': form
    }

    if (request.POST.get('question') == 'Non') and (request.POST.get(fields[-1]) == ''):
        pass

    elif (request.POST.get('question') == 'Non') or ((request.POST.get('question') == 'Oui') and (request.POST.get(fields[-1]) != None)):

        for field in fields:
            if request.POST.get(field) != None:
                request.session.update({field: request.POST.get(field)})
            else:
                pass

        if request.POST.get('question') == 'Oui':
            request.session.update({'reponse': 'Oui'})

        data = {key: value for key, value in request.session.items() if key in fields}

        labels = []
        
        for model in models:
            for field_name in fields:
                try:
                    labels.append(getattr(model, field_name).field.verbose_name)
                except AttributeError:
                    pass

        data_front = {label: value for label, value in zip(labels, data.values())}

        context.update({'data_front': data_front})

    elif request.POST.get('recommencer') != None:

        # Since we restart the form, we better have to clean request.session before

        if 'reponse' in dict(request.session.items()):
            del request.session['reponse']

        for field in fields:
            try:
                del request.session[field]
            except KeyError:
                pass

        return redirect('ajout_culture')

    elif request.POST.get('sauvegarder') != None:

        data = {key: value for key, value in request.session.items() if key in fields}

        data_back = {}

        for key, value in data.items():
            if key.endswith('date') and (value != ''):
                data_back.update({key: dt.strptime(value, '%d-%m-%Y').strftime('%Y-%m-%d')})
            elif (key.endswith('date')) and (value == ''):
                data_back.update({key: None})
            else:
                data_back.update({key: value})

        instance = Culture()

        for key, value in data_back.items():
            setattr(instance, key, value)
        instance.save()

        if ('reponse' in dict(request.session.items())) and (request.session['reponse'] == 'Oui'):

            data_back.update({'nom_culture': Culture.objects.get(nom = data['nom'])})

            instance = PhaseCulture()

            for key, value in data_back.items():
                setattr(instance, key, value)
            instance.save()

        # Once data are saved, we can clean request.session

        for field in fields:
            try:
                del request.session[field]
            except KeyError:
                pass
        
        return redirect('etat_jardin')

    return render(request, template_name, context)

def ajout_graine(request):
    template_name = 'forms/one_step_form.html'

    form = AddGraine(request.POST or None)

    model = Graine

    fields = ['type_graine', 'espece_graine', 'variete_graine', 'niveau_stock', 'provenance', 'annee_recolte', 'remarques']

    context = {
        'form': form
    }

    if request.POST.get('confirmation_step') != None:

        for field in fields:
            if request.POST.get(field) != None:
                request.session.update({field: request.POST.get(field)})
            else:
                pass
        
        data = {key: value for key, value in request.session.items() if key in fields}

        labels = []

        for field_name in fields:
            labels.append(getattr(model, field_name).field.verbose_name)

        data_front = {label: value for label, value in zip(labels, data.values())}

        context.update({'data_front': data_front})

    if request.POST.get('recommencer') != None:

        for field in fields:
            try:
                del request.session[field]
            except KeyError:
                pass

        return redirect('ajout_graine')

    if request.POST.get('sauvegarder') != None:

        data = {key: value for key, value in request.session.items() if key in fields}
        data.update({'nom_usuel': data['espece_graine'] +' '+ data['variete_graine']})
        data['nom_usuel'] = data['nom_usuel'].strip()

        instance = Graine()

        for key, value in data.items():
            setattr(instance, key, value)
        instance.save()

        for field in fields:
            try:
                del request.session[field]
            except KeyError:
                pass

        return redirect('ressources_jardin')

    return render(request, template_name, context)

def actualiser_lot(request, nom_culture, id):
    template_name = 'forms/one_step_form.html'

    form = ActualiserLot(request.POST or None)

    model = EtatLot

    fields = ['etat', 'date', 'quantite', 'remarques']

    context = {
        'culture_name_data': nom_culture,
        'id_data': id,
        'form': form
    }

    if request.POST.get('confirmation_step') != None:

        for field in fields:
            if request.POST.get(field) != None:
                request.session.update({field: request.POST.get(field)})
            else:
                pass
        
        data = {key: value for key, value in request.session.items() if key in fields}

        labels = []

        for field_name in fields:
            labels.append(getattr(model, field_name).field.verbose_name)

        data_front = {label: value for label, value in zip(labels, data.values())}

        context.update({'data_front': data_front})

    if request.POST.get('recommencer') != None:

        for field in fields:
            try:
                del request.session[field]
            except KeyError:
                pass

        return redirect('actualiser_lot', nom_culture = nom_culture, id = id)

    elif request.POST.get('sauvegarder') != None:

        id_lot = model.objects.values('id_lot').filter(id = id).last()['id_lot']

        data = {key: value for key, value in request.session.items() if key in fields}
        data.update({
            'nom_culture': nom_culture,
            'id_lot': id_lot
        })
        if 'etat' not in data:
            data.update({'etat': ''})

        '''
        Une fois qu'un lot passe à l'état Récoltable, il est de temps en temps... récolté.
        Cela signifie que lorsque l'agriculteur récolte un plant de ce lot, il rentre
        dans l'application la quantité récolté du lot. Cette quantité est ensuite soustrait
        de sorte à conserver en donnée la différence entre la quantité précédente et la quantité récoltée.
        '''

        if (data['etat'] == 'Récolté') and (data['quantite'] != ''):
            quantite_recoltable = model.objects.values('quantite').filter(id = id).last()['quantite']

            quantite_recoltee = quantite_recoltable - int(data['quantite'])

            data.update({
                'quantite': quantite_recoltee,
                'etat': 'Récoltable'
            })

        data_back = {}

        for key, value in data.items():
            if (key.endswith('date')) and (value != ''):
                data_back.update({key: dt.strptime(value, '%d-%m-%Y').strftime('%Y-%m-%d')})
            elif (key.endswith('date')) and (value == ''):
                date = model.objects.values('date').filter(id = id).last()['date']
                data_back.update({key: date})
            elif key == 'quantite':
                if value == '':
                    quantite = model.objects.values('quantite').filter(id = id).last()['quantite']
                    data_back.update({
                        key: quantite,
                        'quantite_etat': quantite
                    })
                else:
                    data_back.update({
                        key: value,
                        'quantite_etat': value
                    })
            elif (key == 'etat') and (value == ''):
                    etat = model.objects.values('etat').filter(id = id).last()['etat']
                    data_back.update({key: etat})
            elif key == 'id_lot':
                data_back.update({key: Lot.objects.get(id = id_lot)})
            elif key == 'nom_culture':
                data_back.update({key: Culture.objects.get(nom = value)})
            else:
                data_back.update({key: value})

        instance = model()

        for key, value in data_back.items():
            setattr(instance, key, value)
        instance.save()

        for field in fields:
            try:
                del request.session[field]
            except KeyError:
                pass

        return redirect('etat_jardin_detail', nom_culture = nom_culture)

    return render(request, template_name, context)

def actualiser_culture(request, nom_culture):
    template_name = 'forms/one_step_form.html'

    form = ActualiserCulture(request.POST or None)

    fields = ['nom_culture', 'phase', 'phase_date']

    context = {
        'form': form,
        'culture_name_data': nom_culture
    }

    if request.POST.get('confirmation_step') != None:

        for field in fields:
            if request.POST.get(field) != None:
                request.session.update({field: request.POST.get(field)})
            else:
                pass

        data = {'nom_culture': nom_culture}

        data.update({key: value for key, value in request.session.items() if key in fields})

        labels = []

        for field_name in fields:
            labels.append(getattr(PhaseCulture, field_name).field.verbose_name)

        data_front = {label: value for label, value in zip(labels, data.values())}

        context.update({'data_front': data_front})

    if request.POST.get('recommencer') != None:

        for field in fields:
            try:
                del request.session[field]
            except KeyError:
                pass

        return redirect('actualiser_culture', nom_culture = nom_culture)

    elif request.POST.get('sauvegarder') != None:

        data = {key: value for key, value in request.session.items() if key in fields}

        data.update({'nom_culture': nom_culture})

        data_back = {}

        for key, value in data.items():
            if (key.endswith('date')) and (value != ''):
                data_back.update({key: dt.strptime(value, '%d-%m-%Y').strftime('%Y-%m-%d')})
            elif (key.endswith('date')) and (value == ''):
                data_back.update({key: None})
            elif key == 'nom_culture':
                data_back.update({key: Culture.objects.get(nom = value)})
            else:
                data_back.update({key: value})

        instance = PhaseCulture()

        for key, value in data_back.items():
            setattr(instance, key, value)
        instance.save()

        for field in fields:
            try:
                del request.session[field]
            except KeyError:
                pass

        return redirect('etat_jardin')

    return render(request, template_name, context)

def actualiser_graine(request, id):
    template_name = 'forms/one_step_form.html'

    #data = Graine.objects.filter(id = id)

    data = Graine.objects.values('niveau_stock', 'remarques').filter(id = id)

    print(data)
    print(data[0])

    form = ActualiserGraine(data[0] or None)

    model = Graine

    fields = ['niveau_stock', 'remarques']

    context = {
        'id_data': id,
        'form': form
    }

    if request.POST.get('confirmation_step') != None:

        for field in fields:
            if request.POST.get(field) != None:
                request.session.update({field: request.POST.get(field)})
            else:
                pass
        
        data = {key: value for key, value in request.session.items() if key in fields}

        labels = []

        for field_name in fields:
            labels.append(getattr(model, field_name).field.verbose_name)

        data_front = {label: value for label, value in zip(labels, data.values())}

        context.update({'data_front': data_front})

    if request.POST.get('recommencer') != None:

        for field in fields:
            try:
                del request.session[field]
            except KeyError:
                pass

        return redirect('actualiser_graine', id = id)

    if request.POST.get('sauvegarder') != None:

        data = {key: value for key, value in request.session.items() if key in fields}

        instance = Graine(id)

        for key, value in data.items():
            setattr(instance, key, value)
        instance.save(update_fields = list(data))

        for field in fields:
            try:
                del request.session[field]
            except KeyError:
                pass

        return redirect('ressources_jardin')

    return render(request, template_name, context)