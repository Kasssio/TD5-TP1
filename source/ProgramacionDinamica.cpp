#include "ProgramacionDinamica.h"
#include <vector>
#include <iostream>
using namespace std;

std::vector<int> encontrarSeamPD(const std::vector<std::vector<double>>& energia) {
    int n = energia.size();
    int m = energia[0].size();
    vector<vector<double>> solution(n,vector<double>(m));
    solution[0] = energia[0]; // Caso base de tabla.
    /* 
    Hacemos enfoque bottom-up para construir la tabla. El camino mínimo va a ser construido en base al mínimo 
    entre tres celdas arriba de la celda i,j más la energía de esta: i-1,j-1 , i-1,j y i-1,j+1.
    */
    for(int i = 1; i< n; i++){ // O(n*m)
        for(int j = 0; j<m; j++){
            double e = energia[i][j];
            if(j == 0) solution[i][j] = e + min(solution[i-1][j],solution[i-1][j+1]);
            else if(j == m-1) solution[i][j] = e + min(solution[i-1][j-1], solution[i-1][j]);
            else solution[i][j] = e + min(min(solution[i-1][j-1], solution[i-1][j]),solution[i-1][j+1]);
        }
    }
    /* Ahora tengo que reconstruir el camino, pero tengo que encontrar la mínima energía primero. 
    Esto lo puedo buscar en la última fila. */
    double minimo = 1e18; 
    int minPos;
    for(int i=0; i<m; i++){ // Buscamos la menor energía.
        if(solution[n-1][i] < minimo) {
            minimo = solution[n-1][i];
            minPos = i;

        }
    }
    vector<int> res(n);
    res[n-1] = minPos;
    /* Ahora podemos reconstruir el camino. Tenemos que buscar cuál de las tres celdas superiores 
    es igual a solution[i][minPos] - energia[i][minPos].
    */
    for(int i = n-1; i > 0; i--){
        double prev = solution[i][minPos] - energia[i][minPos];
        if(minPos > 0){ // Descartamos minPos=0, podemos considerar la celda de arriba a la izquierda.
            if(solution[i-1][minPos-1] == prev) minPos = minPos - 1; //  Si coincide el de la izquierda, nos quedamos con la izquierda.
        }
        if(minPos < m-1){ // Descartamos minPos=m-1, podemos considerar la celda de arriba a la derecha.
            if (solution[i-1][minPos+1] == prev) minPos = minPos + 1; // Si coincide el de la derecha, nos quedamos con la derecha.
        }  
        res[i-1] = minPos; // Agregamos la columna al camino
    }
    return res;
}
