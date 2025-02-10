# Calcul de l'ensemble de Mandelbrot en python
import numpy as np
from dataclasses import dataclass
from PIL import Image
from math import log
from time import time
import matplotlib.cm
from mpi4py import MPI

comm = MPI.COMM_WORLD.Dup()
rank = comm.Get_rank()
nbp = comm.Get_size()


class MandelbrotSet:

    def __init__(self, max_iterations : int, escape_radius : float = 2. ):
        self.max_iterations = max_iterations
        self.escape_radius  = escape_radius

    def __contains__(self, c: complex) -> bool:
        return self.stability(c) == 1

    def convergence(self, c: np.ndarray, smooth=False, clamp=True) -> np.ndarray:
        value = self.count_iterations(c, smooth)/self.max_iterations
        return np.maximum(0.0, np.minimum(value, 1.0)) if clamp else value

    def count_iterations(self, c: complex,  smooth=False) -> int | float:
        z:    complex
        iter: int

        # On vérifie dans un premier temps si le complexe
        # n'appartient pas à une zone de convergence connue :
        #   1. Appartenance aux disques  C0{(0,0),1/4} et C1{(-1,0),1/4}
        if c.real*c.real+c.imag*c.imag < 0.0625:
            return self.max_iterations
        if (c.real+1)*(c.real+1)+c.imag*c.imag < 0.0625:
            return self.max_iterations
        #  2.  Appartenance à la cardioïde {(1/4,0),1/2(1-cos(theta))}
        if (c.real > -0.75) and (c.real < 0.5):
            ct = c.real-0.25 + 1.j * c.imag
            ctnrm2 = abs(ct)
            if ctnrm2 < 0.5*(1-ct.real/max(ctnrm2, 1.E-14)):
                return self.max_iterations
        # Sinon on itère
        z = 0
        for iter in range(self.max_iterations):
            z = z*z + c
            if abs(z) > self.escape_radius:
                if smooth:
                    return iter + 1 - log(log(abs(z)))/log(2)
                return iter
        return self.max_iterations


# On peut changer les paramètres des deux prochaines lignes
mandelbrot_set = MandelbrotSet(max_iterations=50, escape_radius=10)
width, height = 1024, 1024

scaleX = 3./width
scaleY = 2.25/height
convergence = np.empty((width, height), dtype=np.double)
line = np.empty(width)

# Calcul de l'ensemble de mandelbrot :
deb = time()

row_ind = 0
if rank==0:
    fin = time()
    #initilisation
    for k in range(1,nbp):
        comm.send(row_ind, dest=k)
        row_ind +=1
    while (row_ind<height):
        status = MPI.Status()
        line = comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
        convergence[:, status.tag] = line
        comm.send(row_ind, dest=status.source)
        row_ind += 1
    for k in range (1,nbp):
        comm.send(-1,k)
    fin= time()
    print(f"Temps du calcul de l'ensemble de Mandelbrot : {fin - deb}")

if rank>0:
    #initialisation
    while True :
        row_ind = comm.recv(source=0)
        if row_ind == -1 :
            break
        for x in range(width):
            c = complex(-2. + scaleX*x, -1.125 + scaleY * row_ind)
            line[x] = mandelbrot_set.convergence(c, smooth=True)
        comm.send(line, dest=0, tag=row_ind)



# Constitution de l'image résultante :
if rank==0:
    deb = time()
    image = Image.fromarray(np.uint8(matplotlib.cm.plasma(convergence.T)*255))
    fin = time()
    print(f"Temps de constitution de l'image : {fin-deb}")
    image.show()
