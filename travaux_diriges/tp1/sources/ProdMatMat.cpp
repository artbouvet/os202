#include <algorithm>
#include <cassert>
#include <iostream>
#include <thread>
#if defined(_OPENMP)
#include <omp.h>
#endif
#include "ProdMatMat.hpp"

namespace {
void prodSubBlocks(int iRowBlkA, int iColBlkB, int iColBlkA, int szBlock,
                   const Matrix& A, const Matrix& B, Matrix& C) {
  #pragma omp parallel for collapse(2)
  for (int k = iColBlkA; k < std::min(A.nbCols, iColBlkA + szBlock); k++)
    for (int j = iColBlkB; j < std::min(B.nbCols, iColBlkB + szBlock); j++)
      for (int i = iRowBlkA; i < std::min(A.nbRows, iRowBlkA + szBlock); ++i)
        C(i, j) += A(i, k) * B(k, j);
}
const int szBlock = 32;
}  // namespace

void prodSubBlocks2(int iRowBlkA, int iColBlkB, int iColBlkA, int szBlock,
                   const Matrix& A, const Matrix& B, Matrix& C) {
    // Calcul du produit des sous-blocs
    for (int k = 0; k < A.nbCols / szBlock; ++k) {
        for (int i = iRowBlkA; i < iRowBlkA + szBlock; ++i) {
            for (int j = iColBlkB; j < iColBlkB + szBlock; ++j) {
                for (int l = 0; l < szBlock; ++l) {
                    C(i, j) += A(i, k * szBlock + l) * B(k * szBlock + l, j);
                }
            }
        }
    }
}

void prodMatrixMatrixBlocking(const Matrix& A, const Matrix& B, Matrix& C, int szBlock) {
    int n = A.nbRows;
    // Boucles sur les blocs de A et B
    for (int iRowBlkA = 0; iRowBlkA < n; iRowBlkA += szBlock) {
        for (int iColBlkB = 0; iColBlkB < n; iColBlkB += szBlock) {
            for (int iColBlkA = 0; iColBlkA < n; iColBlkA += szBlock) {
                prodSubBlocks(iRowBlkA, iColBlkB, iColBlkA, szBlock, A, B, C);
            }
        }
    }
}


Matrix operator*(const Matrix& A, const Matrix& B) {
  Matrix C(A.nbRows, B.nbCols, 0.0);
  prodSubBlocks(0, 0, 0, std::max({A.nbRows, B.nbCols, A.nbCols}), A, B, C);
  return C;
}
