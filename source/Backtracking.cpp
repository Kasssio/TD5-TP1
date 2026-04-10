#include "Backtracking.h"
#include <iostream>
#include <vector>
using namespace std;
void Backtracking(const std::vector<std::vector<double>>& energia,int i, int j,pair<vector<int>, double> curr,pair<vector<int>, double>& best) {
    int n = energia.size();
    int m = energia[0].size();
    curr.first.push_back(j);
    curr.second += energia[i][j];
    if (curr.second >= best.second) return; // Poda de optimalidad.
    if (i == n-1){ 
        best = curr;
        return;
    }

    for (int k = -1; k <= 1; k++) {
        int col = j + k;
        if (col >= 0 && col < m) {
            Backtracking(energia, i + 1, col, curr, best);
        }
    }
}

std::vector<int> encontrarSeamBacktracking(const std::vector<std::vector<double>>& energia) {
    int m = energia[0].size();
    pair<vector<int>, double> bestSeam;
    bestSeam.second = 1e18;

    for (int i = 0; i < m; i++) {
        pair<vector<int>, double> curr;
        Backtracking(energia, 0, i, curr, bestSeam);
    }

    return bestSeam.first;
}