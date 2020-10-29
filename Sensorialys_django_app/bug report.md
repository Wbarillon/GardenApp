Dans l'ajout d'un lot, si on sélectionne l'état planté et qu'on sélectionne des données pour la date et la phase lunaire, ça enregistre. Mettons que l'utilisateur décide de prendre l'état semé, ça conservera les données de l'état planté.

Solution : à l'heure actuelle, si le lot a été mal pris suggéré à l'utilisateur de reprendre à 0 la saisie du lot.

Si quantité au-delà de la limite de smallintegerfield de la bdd, ça crash.

Solution : Mettre un charfield et convertir dans data_back la chaîne de caractère en nombre. Non seulement le charfield accepte les valeurs nulles, mais il gère aussi la quantité. Avec max_length = 4, on ne peut pas mettre plus de 9999 graines.

Quand on actualise un lot, si on ne change pas la date du jour, le lot ne s'actualise pas.

Solution : changer la date lors de l'actualisation du lot. Autrement dit, ne pas actualiser un lot plus d'une fois par jour.