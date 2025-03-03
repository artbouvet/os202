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



Avec notre code final parallélisé (asynchrone, c'est à dire que le processus de calcul n'attend pas le processus d'affichage et le processus d'affichage n'affiche pas toutes itérations de calcul), on observe bien une alternance calcul/affichage avec plusieurs itérations de calcul entre 2 itérations d'affichage, ce qui était attendu étant donné que le processus d'affichage prend plus de temps que celui de calcul (cela se voit davantage pour des itérations plus élevées)

Pattern : u, resolution : (800, 800), iterations : 1, moyenne temps affichage : 0.0055408477783203125
Pattern : u, resolution : (800, 800), iterations : 10, moyenne temps calcul : 0.006296911599144103
Pattern : u, resolution : (800, 800), iterations : 11, moyenne temps calcul : 0.006572068313843588
Pattern : u, resolution : (800, 800), iterations : 2, moyenne temps affichage : 0.008676767349243164
Pattern : u, resolution : (800, 800), iterations : 12, moyenne temps calcul : 0.006666323125448405
Pattern : u, resolution : (800, 800), iterations : 13, moyenne temps calcul : 0.00681207023684226
Pattern : u, resolution : (800, 800), iterations : 3, moyenne temps affichage : 0.010689258575439453
Pattern : u, resolution : (800, 800), iterations : 14, moyenne temps calcul : 0.00688458354468615
Pattern : u, resolution : (800, 800), iterations : 15, moyenne temps calcul : 0.007019973508471957
Pattern : u, resolution : (800, 800), iterations : 4, moyenne temps affichage : 0.012926340103149414
Pattern : u, resolution : (800, 800), iterations : 16, moyenne temps calcul : 0.007085672728175631
Pattern : u, resolution : (800, 800), iterations : 17, moyenne temps calcul : 0.00726250919075749
Pattern : u, resolution : (800, 800), iterations : 5, moyenne temps affichage : 0.01452493667602539
Pattern : u, resolution : (800, 800), iterations : 18, moyenne temps calcul : 0.007318828957331926
Pattern : u, resolution : (800, 800), iterations : 19, moyenne temps calcul : 0.007425402062190324
Pattern : u, resolution : (800, 800), iterations : 6, moyenne temps affichage : 0.015455007553100586
Pattern : u, resolution : (800, 800), iterations : 20, moyenne temps calcul : 0.00752924527431801
Pattern : u, resolution : (800, 800), iterations : 21, moyenne temps calcul : 0.007625532320478026
Pattern : u, resolution : (800, 800), iterations : 7, moyenne temps affichage : 0.016310146876743863
Pattern : u, resolution : (800, 800), iterations : 22, moyenne temps calcul : 0.007709845799814851
Pattern : u, resolution : (800, 800), iterations : 23, moyenne temps calcul : 0.007797656399100475
Pattern : u, resolution : (800, 800), iterations : 8, moyenne temps affichage : 0.01722570402281625
Pattern : u, resolution : (800, 800), iterations : 24, moyenne temps calcul : 0.007880695603380056
Pattern : u, resolution : (800, 800), iterations : 25, moyenne temps calcul : 0.00792129351902947
Pattern : u, resolution : (800, 800), iterations : 9, moyenne temps affichage : 0.01797513308979216
Pattern : u, resolution : (800, 800), iterations : 26, moyenne temps calcul : 0.00794588731245833
Pattern : u, resolution : (800, 800), iterations : 27, moyenne temps calcul : 0.007982789210312606
Pattern : u, resolution : (800, 800), iterations : 10, moyenne temps affichage : 0.018637865214120773
Pattern : u, resolution : (800, 800), iterations : 28, moyenne temps calcul : 0.008058887311792273
Pattern : u, resolution : (800, 800), iterations : 29, moyenne temps calcul : 0.008140097612632454
Pattern : u, resolution : (800, 800), iterations : 11, moyenne temps affichage : 0.019323145233707508
Pattern : u, resolution : (800, 800), iterations : 30, moyenne temps calcul : 0.008177322700116178
Pattern : u, resolution : (800, 800), iterations : 31, moyenne temps calcul : 0.008242534026961408
Pattern : u, resolution : (800, 800), iterations : 12, moyenne temps affichage : 0.019909317178643623
Pattern : u, resolution : (800, 800), iterations : 32, moyenne temps calcul : 0.008275018558363996
Pattern : u, resolution : (800, 800), iterations : 33, moyenne temps calcul : 0.008306157469755746
Pattern : u, resolution : (800, 800), iterations : 13, moyenne temps affichage : 0.020417552229725355
Pattern : u, resolution : (800, 800), iterations : 34, moyenne temps calcul : 0.00835541194327367
Pattern : u, resolution : (800, 800), iterations : 35, moyenne temps calcul : 0.008433858467757486
Pattern : u, resolution : (800, 800), iterations : 14, moyenne temps affichage : 0.02113287608662407
Pattern : u, resolution : (800, 800), iterations : 36, moyenne temps calcul : 0.008462091201166096
Pattern : u, resolution : (800, 800), iterations : 37, moyenne temps calcul : 0.008533217262682935
Pattern : u, resolution : (800, 800), iterations : 15, moyenne temps affichage : 0.021693954476109747
Pattern : u, resolution : (800, 800), iterations : 38, moyenne temps calcul : 0.008562944294993019
Pattern : u, resolution : (800, 800), iterations : 39, moyenne temps calcul : 0.00866828251387761
Pattern : u, resolution : (800, 800), iterations : 16, moyenne temps affichage : 0.022113288053265814
Pattern : u, resolution : (800, 800), iterations : 40, moyenne temps calcul : 0.008757093434592942
Pattern : u, resolution : (800, 800), iterations : 41, moyenne temps calcul : 0.008831416065312382
Pattern : u, resolution : (800, 800), iterations : 17, moyenne temps affichage : 0.022586226366469512
Pattern : u, resolution : (800, 800), iterations : 42, moyenne temps calcul : 0.008868427711401481
Pattern : u, resolution : (800, 800), iterations : 43, moyenne temps calcul : 0.008915490429992505
Pattern : u, resolution : (800, 800), iterations : 18, moyenne temps affichage : 0.023034095667311797
Pattern : u, resolution : (800, 800), iterations : 44, moyenne temps calcul : 0.008950418751830884
Pattern : u, resolution : (800, 800), iterations : 45, moyenne temps calcul : 0.009029822735052997
Pattern : u, resolution : (800, 800), iterations : 19, moyenne temps affichage : 0.02347095379430347
Pattern : u, resolution : (800, 800), iterations : 46, moyenne temps calcul : 0.009074712807087751
Pattern : u, resolution : (800, 800), iterations : 47, moyenne temps calcul : 0.009138928568637681
Pattern : u, resolution : (800, 800), iterations : 20, moyenne temps affichage : 0.02392496237355762
Pattern : u, resolution : (800, 800), iterations : 48, moyenne temps calcul : 0.00917153230932982
Pattern : u, resolution : (800, 800), iterations : 49, moyenne temps calcul : 0.009265868215689433
Pattern : u, resolution : (800, 800), iterations : 21, moyenne temps affichage : 0.024361211606985123
Pattern : u, resolution : (800, 800), iterations : 50, moyenne temps calcul : 0.009337093382010234
Pattern : u, resolution : (800, 800), iterations : 51, moyenne temps calcul : 0.009376572693784993
Pattern : u, resolution : (800, 800), iterations : 22, moyenne temps affichage : 0.0246805299448591
Pattern : u, resolution : (800, 800), iterations : 52, moyenne temps calcul : 0.009396127602243997
Pattern : u, resolution : (800, 800), iterations : 53, moyenne temps calcul : 0.009481625404402567
Pattern : u, resolution : (800, 800), iterations : 23, moyenne temps affichage : 0.025078709704009067
Pattern : u, resolution : (800, 800), iterations : 54, moyenne temps calcul : 0.009519163085134447
Pattern : u, resolution : (800, 800), iterations : 55, moyenne temps calcul : 0.009574012362977575