#include "FuerzaBruta.h"
using namespace std;
#include <iostream>

vector<int> FuerzaBruta(const vector<vector<double>>& energia, int i, int j){ 
    int n = energia.size();
    int m = energia[0].size();
    if (i == n - 1){
        return {j+1};
    }
    vector<int> best;
    double minEnergy = 1e18; // establecemos energia mínima para empezar a comparar
    for(int k = -1; k <= 1; k++){
        if (j+k >= 0 && j+k < m){
            vector<int> candidate = FuerzaBruta(energia,i+1,j+k); // salto recursivo 
            double candidateEnergy = 0;
            int auxI = i+1; // fila inicial para recorrer el candidato
            for(int c : candidate){ // reconstruimos la energia del candidato para ver si es el óptimo
                candidateEnergy += energia[auxI][c-1];
                auxI++;
            }
            if(candidateEnergy<minEnergy){ // poda de optimalidad, vemos si el candidato es mejor al camino que conseguimos hasta ahora.
                minEnergy = candidateEnergy;
                best = candidate;
            }
        }
    }
    // ahora tenemos que armar el path
    vector<int> currPath = {j+1};
    for (int c : best) {
        currPath.push_back(c);
    }
    return currPath;
}
std::vector<int> encontrarSeamFuerzaBruta(const std::vector<std::vector<double>>& energia) {
    if (energia.empty()) return {};
    int m = energia[0].size();
    // hacemos lo mismo que en la recursión para encontrar la columna óptima de la primera columna
    vector<int> best;
    double minEnergy = 1e18;
    for(int j = 0; j < m; j++){ //avanzo columnas
        vector<int> candidate = FuerzaBruta(energia,0,j);
        double totalEnergy = 0;
        for (int i = 0; i < candidate.size(); i++) { // calculamos energia de la costura
            totalEnergy += energia[i][candidate[i] - 1];
        }
        if(totalEnergy < minEnergy) {
            minEnergy = totalEnergy;
            best = candidate;
        }
    }
    return best;
}
