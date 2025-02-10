# Produit matrice-vecteur v = A.u
import numpy as np
from mpi4py import MPI
from time import time 

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
nbp = comm.Get_size()

deb = time()
# Dimension du problème (peut-être changé)
dim = 120
# Initialisation de la matrice
A = np.array([[(i+j) % dim+1. for i in range(dim)] for j in range(dim)])
print(f"A = {A}")

# Initialisation du vecteur u
u = np.array([i+1. for i in range(dim)])
print(f"u = {u}")

# Produit matrice-vecteur
"""v = A.dot(u)
print(f"v = {v}")"""

nb_ligne_par_processeur = dim // nbp
debut = rank * nb_ligne_par_processeur
fin = debut + nb_ligne_par_processeur if rank < nbp - 1 else dim

##### Vecteur par colonne #####
"""
matrices_partielles = A[debut:fin,:].dot(u)
resultat = comm.gather(matrices_partielles, root=0)

if rank == 0:
    produit = np.hstack(resultat)
    fin = time()
    print(f"Temps de calcul : {fin-deb}")
"""
##### Vecteur par ligne #####

matrices_partielles = A[:,debut:fin].dot(u[debut:fin])
resultat = comm.gather(matrices_partielles, root=0)

if rank == 0 :
    produit = resultat[0]
    for k in range(1,nbp):
        produit += resultat[k]
    fin = time()
    print(f"Temps de calcul : {fin-deb}")