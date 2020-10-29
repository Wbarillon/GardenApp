from unicodedata2 import normalize

from django import forms

from functools import partial

from .models import *


DatePicker = partial(forms.DateInput, {'class': 'datepicker'})


class AddCulture(forms.Form):

    type_contenant = forms.ChoiceField(
        choices = TypeContenantCulturesChoix.choices,
        label = 'Type de contenant'
    )

    nom = forms.CharField(
        label = 'Nom (sans espace)'
    )

    question = forms.BooleanField(
        label = 'Souhaites-tu noter une rotation de culture ?',
        widget = forms.RadioSelect(
            choices = [
                ('Oui', 'Oui'),
                ('Non', 'Non')
            ],
            attrs = {'class': 'radio-check'}
        ),
        required = False
    )

    def __init__(self, *args, **kwargs):

        reponse = kwargs.pop('reponse')

        super(AddCulture, self).__init__(*args, **kwargs)

        if reponse == 'Oui':
            self.fields['phase'] = forms.ChoiceField(
                choices = PhaseCulturesChoix.choices,
                required = False,
            )

            self.fields['phase_date'] = forms.DateField(
                widget = DatePicker(),
                required = False
            )

class AddLotStep1(forms.Form):

    question = forms.BooleanField(
        label = 'Que veux-tu faire ?',
        widget = forms.RadioSelect(
            choices = [
                ('lot_parent', 'Semer'),
                ('lot_enfant', 'Repiquer'),
                ('lot_parent', 'Planter une plante de l\'extérieur')
            ],
            attrs = {'class': 'radio-check'}
        ),
        required = False
    )

class AddLotStep2(forms.ModelForm):

    class Meta:
        model = Lot
        fields = ['id_graine']

class AddLotStep3(forms.Form):

    quantite = forms.CharField(
        max_length = 4,
        label = 'Indique la quantité',
        required = False
    )

    remarques = forms.CharField(
        max_length = 150,
        label = 'Quantité non-numérique (sillon : 1m)',
        required = False
    )

class AddLotStep4(forms.ModelForm):

    class Meta:
        model = EtatLot
        fields = ['etat']
        labels = {
            'etat': 'Le lot est-il semé ou planté ?'
        }
        widgets = {
            'etat': forms.RadioSelect(
                choices = [
                    ('Semé', 'Semé'),
                    ('Planté', 'Planté')
                ],
                attrs = {'class': 'radio-check'}
            )
        }

    def __init__(self, *args, **kwargs):

        etat = kwargs.pop('etat', None)

        super(AddLotStep4, self).__init__(*args, **kwargs)

        if etat != None:

            self.fields['date'] = forms.DateField(
                label = 'Date',
                widget = DatePicker(),
                required = False
            )

            self.fields['phase_lunaire'] = forms.ChoiceField(
                label = 'Phase lunaire',
                choices = PhasesLunairesChoix.choices,
                required = False
            )

            self.fields['constellation'] = forms.ChoiceField(
                label = 'Constellation',
                choices = ConstellationChoix.choices,
                required = False
            )

            self.fields['perigee_apogee'] = forms.ChoiceField(
                label = 'Périgée / Apogée',
                choices = PerigeeApogeeChoix.choices,
                required = False
            )

            self.fields['lunar_node'] = forms.ChoiceField(
                label = 'Noeud lunaire',
                choices = BooleenChoix.choices,
                required = False
            )

class AddGraine(forms.ModelForm):

    class Meta:
        model = Graine
        fields = ['espece_graine', 'variete_graine', 'type_graine', 'niveau_stock', 'provenance', 'annee_recolte', 'remarques']
        widgets = {
            'niveau_stock': forms.Select(choices = NiveauStockGraineChoix.choices)
        }

class ActualiserCulture(forms.ModelForm):

    class Meta:
        model = PhaseCulture
        fields = ['phase', 'phase_date']
        labels = {
            'phase': PhaseCulture.phase.field.verbose_name,
            'phase_date': PhaseCulture.phase_date.field.verbose_name
        }
        widgets = {
            'phase': forms.RadioSelect(
                choices = PhaseCulturesChoix.choices,
                attrs = {'class': 'radio-check'}
            ),
            'phase_date': DatePicker()
        }

class ActualiserLot(forms.ModelForm):

    class Meta:
        model = EtatLot
        fields = ['etat', 'date', 'quantite', 'remarques']
        labels = {
            'etat': 'Que s\'est-il passé ?',
            'date': 'Date'
        }
        widgets = {
            'etat': forms.RadioSelect(
                choices = EtatLotsChoix.choices,
                attrs = {'class': 'radio-check'}
            ),
            'date': DatePicker()
        }

class ActualiserGraine(forms.ModelForm):
    
    class Meta:
        model = Graine
        fields = ['niveau_stock', 'remarques']
        widgets = {
            'niveau_stock': forms.Select(choices = NiveauStockGraineChoix.choices)
        }
