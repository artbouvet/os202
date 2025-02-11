"""
TP3 OS202 - Arthur BOUVET

exécution avec : mpiexec -n 16 python bucket_sort.py, en changeant la valeur 16 par le nombre de processus parallèles souhaités
"""

import numpy as np
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
nbp = comm.Get_size()

dim = 50
maxi=100

## On génère un tableau de valeurs aléatoires (un tableau pour chaque processus)
values = np.random.randint(1,maxi,dim)
values.sort()
#print(values)

## On calcule les quantiles locaux (pour chaque processus) puis globaux pour le tableau général
quantiles = np.quantile(values, np.linspace(0, 1, nbp + 1))
#print(f"Quantiles : {quantiles}")

all_quantiles = np.zeros(nbp*(nbp+1),dtype="float")
comm.Allgather(quantiles, all_quantiles)
all_quantiles.sort()

global_quantiles = np.quantile(all_quantiles, np.linspace(0, 1, nbp + 1))
#print(f"Global Quantiles : {global_quantiles}")

## On place chaque valeur dans un bucket local (intervalle entre 2 quantiles)
buckets = []
for i in range(0,nbp-1):
    buckets.append(values[(values >= global_quantiles[i]) & (values < global_quantiles[i+1])]) #borne sup stricte pour ne pas compter 2 fois la même valeur
buckets.append(values[(values >= global_quantiles[nbp-1]) & (values <= global_quantiles[nbp])]) #sauf pour le dernier bucket
#print(f"Buckets : {buckets}")

## On envoie les buckets à tous les processus
all_buckets = comm.alltoall(buckets)
all_buckets = np.concatenate(all_buckets)
all_buckets.sort()
#print(f"All Buckets {rank}: {all_buckets}")

## On rassemble les buckets triés par chaque processus en local pour former le tableau final trié
if rank == 0:
    all_final_buckets = comm.gather(all_buckets, root=0)
    liste_triee = np.concatenate(all_final_buckets)
    liste_triee.sort()
    print("Tableau final :", liste_triee)
else:
    comm.gather(all_buckets, root=0)