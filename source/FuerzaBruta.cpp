#include "FuerzaBruta.h"
#include <iostream>
using namespace std;

vector<int> best;
int n;
int m;
double minEnergy = __DBL_MAX__;
void FuerzaBruta(const vector<vector<double>>& energia, int i, int j, pair<vector<int>,double> currSeam){ // O(3^n) 
    if(j < 0 || j >= m) return; // Chequeo fuera de rango. O(1).
    currSeam.first.push_back(j); // O(1) amortizado
    currSeam.second += energia[i][j]; // O(1)
    if(i == n-1){ // Caso base, llegamos al final. O(1).
        if(currSeam.second < minEnergy) { // Reemplazamos el mejor si encontramos un mejor resultado. O(1).
            minEnergy = currSeam.second; // O(1)
            best = currSeam.first; // O(1)
        }
        return; // O(1)
    }
    for(int k=-1; k<=1;k++) { // Recorremos energia[i+1][j-1], energia[i+1][j] y energia[i+1][j+1] recursivamente. O(1).
        FuerzaBruta(energia, i+1,j+k,currSeam);
    }
}
std::vector<int> encontrarSeamFuerzaBruta(const std::vector<std::vector<double>>& energia) { // Complejidad final: O(m*3^n).
    if (energia.empty()) return {};
    // Definimos variables globales.
    n = energia.size();
    m = energia[0].size();
    minEnergy = __DBL_MAX__;
    best.clear();
    // Vemos cuál de las m columnas de la primera fila nos da la costura de mínima energía.
    for(int i = 0; i < m; i++){ // O(m)
        FuerzaBruta(energia,0,i,{{},0}); // O(3^n)
    }
    return best;
}
