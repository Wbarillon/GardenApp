from django.db import models

## TextChoices
# Graine table

class NiveauStockGraineChoix(models.TextChoices):
    ABONDANT = 'Abondant', 'Abondant'
    MOYEN = 'Moyen', 'Moyen'
    CRITIQUE = 'Critique', 'Critique'
    EPUISE = 'Épuisé', 'Épuisé'

# Culture table

class PhaseCulturesChoix(models.TextChoices):
    ANNEE1 = 'Année 1', 'Année 1'
    ANNEE2 = 'Année 2', 'Année 2'
    ANNEE3 = 'Année 3', 'Année 3'
    ANNEE4 = 'Année 4', 'Année 4'

class TypeContenantCulturesChoix(models.TextChoices):
    ALVEOLE = 'Alvéole', 'Alvéole'
    BAC = 'Bac', 'Bac'
    BARQUETTE = 'Barquette', 'Barquette'
    PLANCHE = 'Planche', 'Planche'
    POT = 'Pot', 'Pot'

# Lot table

class EtatLotsChoix(models.TextChoices):

    '''
    Le choix Semé et Planté sont possibles aussi, mais il n'est pas utile de le proposer pour l'actualisation des lots.
    Les choix dans l'ajout de lot sont entrés en dur puisqu'il n'y en a que deux et qu'ils ne changeront pas.
    '''

    GERME = 'Germé', 'Germé'
    FLEURI = 'Fleuri', 'Fleuri'
    RECOLTABLE = 'Récoltable', 'Récoltable'
    RECOLTE = 'Récolté', 'Récolté'

class PhasesLunairesChoix(models.TextChoices):
    LCM = 'LCM', 'Lune Croissante Montante'
    LDM = 'LDM', 'Lune Décroissante Montante'
    LCD = 'LCD', 'Lune Croissante Descendante'
    LDD = 'LDD', 'Lune Décroissante Descendante'

class ConstellationChoix(models.TextChoices):
    FEUILLE = 'Feuille', 'Feuille'
    FLEUR = 'Fleur', 'Fleur'
    FRUIT = 'Fruit', 'Fruit'
    RACINE = 'Racine', 'Racine'

class PerigeeApogeeChoix(models.TextChoices):
    NO = 'Non', 'Non'
    PERIGEE = 'Périgée', 'Périgée'
    APOGEE = 'Apogée', 'Apogée'

class BooleenChoix(models.TextChoices):
    FALSE = 'Non', 'Non'
    TRUE = 'Oui', 'Oui'

# Create your models here.

class Graine(models.Model):

    id = models.AutoField(primary_key = True),
    type_graine = models.CharField(verbose_name = 'Type', max_length = 50, null = True, blank = True)
    espece_graine = models.CharField(verbose_name = 'Espèce', max_length = 50, null = True, blank = True)
    variete_graine = models.CharField(verbose_name = 'Variété', max_length = 50, null = True, blank = True)
    niveau_stock = models.CharField(verbose_name = 'Niveau du stock', max_length = 8, null = True, blank = True)
    provenance = models.CharField(verbose_name = 'Provenance', max_length = 50, null = True, blank = True)
    annee_recolte = models.CharField(verbose_name = 'Année de récolte', max_length = 4, null = True, blank = True)
    remarques = models.CharField(verbose_name = 'Remarques', max_length = 150, null = True, blank = True)
    nom_usuel = models.CharField(verbose_name = 'Plante', max_length = 50, null = True, blank = True)

    def __int__(self):
        return self.id

    class Meta:
        verbose_name = 'Graine'
        verbose_name_plural = 'Graines'

class Culture(models.Model):

    nom = models.CharField(primary_key = True, verbose_name = 'Nom', max_length = 30)
    type_contenant = models.CharField(verbose_name = 'Type de contenant', max_length = 9, null = True, blank = True)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = 'Culture'
        verbose_name_plural = 'Cultures'

class PhaseCulture(models.Model):

    id = models.AutoField(primary_key = True)
    nom_culture = models.ForeignKey('Culture', on_delete = models.PROTECT, verbose_name = 'Culture', related_name = 'phase_culture_nom_culture', null = False, blank = False)
    phase = models.CharField(verbose_name = 'Phase', max_length = 7, null = True, blank = False)
    phase_date = models.DateField(verbose_name = 'Date de changement de phase', null = False, blank = False)

    def __int__(self):
        return self.id

    class Meta:
        verbose_name = 'Phase de culture'
        verbose_name_plural = 'Phases de culture'

class EtatLot(models.Model):

    id = models.AutoField(primary_key = True)
    id_lot = models.ForeignKey('Lot', on_delete = models.PROTECT, verbose_name = 'Lot', related_name = 'etat_lot_id_lot', null = True, blank = True)
    nom_culture = models.ForeignKey('Culture', on_delete = models.PROTECT, verbose_name = 'Culture', related_name = 'etat_lot_nom_culture', null = True, blank = True)
    etat = models.CharField(verbose_name = 'État', max_length = 50, null = True, blank = True)
    date = models.DateField(verbose_name = 'Date de l\'état', null = True, blank = True)
    phase_lunaire = models.CharField(verbose_name = 'Phase lunaire', max_length = 4, null = True, blank = True)
    constellation = models.CharField(verbose_name = 'Constellation', max_length = 7, null = True, blank = True)
    perigee_apogee = models.CharField(verbose_name = 'Périgée / Apogée', max_length = 1, null = True, blank = True)
    lunar_node = models.CharField(verbose_name = 'Noeud lunaire', max_length = 3, null = True, blank = True)
    quantite = models.PositiveSmallIntegerField(verbose_name = 'Quantité', null = True, blank = True)
    quantite_etat = models.PositiveSmallIntegerField(verbose_name = 'Quantité relatée', null = True, blank = True)
    remarques = models.CharField(verbose_name = 'Remarques', max_length = 150, null = True, blank = True)

    def __int__(self):
        return self.id

    class Meta:
        verbose_name = 'État du lot'
        verbose_name_plural = 'États du lot'

class Lot(models.Model):

    id = models.AutoField(primary_key = True)
    id_graine = models.ForeignKey('Graine', on_delete = models.PROTECT, verbose_name = 'Graine', related_name = 'etat_lot_id_graine', null = True, blank = True)
    nom_culture_initial = models.CharField(verbose_name = 'Nom de culture initial', max_length = 50, null = True, blank = True)
    quantite_lot = models.PositiveSmallIntegerField(verbose_name = 'Quantité', null = True, blank = True)

    def __int__(self):
        return self.id

    class Meta:
        verbose_name = 'Lot'
        verbose_name_plural = 'Lots'
    