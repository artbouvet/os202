## TP4 - Game of life
Author : Arthur BOUVET 

Date : 02-18-2025 
#


temps d'affichage > temps calcul (rapport 5 à 10)
MAIS grande variabilité des mesures (facteur 10 au sein des valeurs pour un même type de temps) : on implémente donc soit un compteur pour calculer le temps total pris par chaque type de temps sur un nombre d'itérations donné ou afficher la moyenne des temps de calcul mis à jour à chaque itération 

Pattern : u, resolution : (800, 800), iterations : 50, moyenne temps calcul : 5.49e-03 secondes, moyenne temps affichage : 2.44e-02 secondes
Pattern : u, resolution : (800, 800), iterations : 100, moyenne temps calcul : 6.25e-03 secondes, moyenne temps affichage : 2.82e-02 secondes
Pattern : u, resolution : (800, 800), iterations : 150, moyenne temps calcul : 7.06e-03 secondes, moyenne temps affichage : 3.05e-02 secondes
Pattern : u, resolution : (800, 800), iterations : 200, moyenne temps calcul : 7.69e-03 secondes, moyenne temps affichage : 3.19e-02 secondes
Pattern : u, resolution : (800, 800), iterations : 250, moyenne temps calcul : 8.02e-03 secondes, moyenne temps affichage : 3.31e-02 secondes

Pattern : u, resolution : (8000, 8000), iterations : 50, moyenne temps calcul : 4.82e-03 secondes, moyenne temps affichage : 1.14e+00 secondes
Pattern : u, resolution : (8000, 8000), iterations : 100, moyenne temps calcul : 5.56e-03 secondes, moyenne temps affichage : 1.30e+00 secondes
Pattern : u, resolution : (8000, 8000), iterations : 150, moyenne temps calcul : 5.96e-03 secondes, moyenne temps affichage : 1.40e+00 secondes
Pattern : u, resolution : (8000, 8000), iterations : 200, moyenne temps calcul : 6.22e-03 secondes, moyenne temps affichage : 1.47e+00 secondes


au début, impression que les temps diffèrent selon qu'on ajoute ou non un sleep : en réalité, pas de grande différence, surtout qu'on compare des microsecondes sur un processeur qui a d'autres threads en arrière plan


1ere approche de parallélisation envisagée (naive): 
1 processus calcul / 1 processus affichage
créer les processus
envoyer les infos de la grille à chaque itération au processus d'affichage
-> le processus calcul va attendre le processus affichage (zone d'attente qui rend la prallélisation non optimale)


le + important = le résultat final alors que affichage sert uniquement à suivre le processus
-> on peut afficher le résultat toutes les X itérations
OU calcul en continu et affichage prend les valeurs de calcul au moment où il en a besoin (pas toutes les X itérations fixées)
(se rapproche d'un algorithme maître esclave)
on déclenche l'envoi de calcul à affichage avec : envoi d'un message par affichage quand il a terminé


étape suivante : paralléliser le calcul par distribution des données : plusieurs ranks de calcul en parallèle et 1 processus d'affichage
on partitionne la grille
on échange les infos des cellules fantômes en début d'itération