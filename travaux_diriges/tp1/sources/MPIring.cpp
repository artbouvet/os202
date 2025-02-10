#include <stdio.h>
#include <mpi.h>
# include <iostream>
# include <cstdlib>
# include <sstream>
# include <string>
# include <fstream>

int main(int argc, char *argv[]) {
    int rank, size, token;
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    if (size < 2) {
        fprintf(stderr, "Ce programme nécessite au moins 2 processus.\n");
        MPI_Abort(MPI_COMM_WORLD, 1);
    }

    if (rank == 0) {
        // Processus 0 initialise le jeton
        token = 1;
        MPI_Send(&token, 1, MPI_INT, 1, 0, MPI_COMM_WORLD);
        printf("Processus %d a envoyé le jeton %d au processus %d\n", rank, token, 1);
    }

    for (int i = 0; i < size; i++) {
        if (rank == i) {
            MPI_Recv(&token, 1, MPI_INT, (rank - 1 + size) % size, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            token++;
            MPI_Send(&token, 1, MPI_INT, (rank + 1) % size, 0, MPI_COMM_WORLD);
            printf("Processus %d a reçu le jeton %d et l'a envoyé au processus %d\n", rank, token, (rank + 1) % size);
        }
        MPI_Barrier(MPI_COMM_WORLD);
    }

    if (rank == 0) {
        MPI_Recv(&token, 1, MPI_INT, size - 1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        printf("Processus %d a reçu le jeton final: %d\n", rank, token);
    }

    MPI_Finalize();
    return EXIT_SUCCESS;
}
