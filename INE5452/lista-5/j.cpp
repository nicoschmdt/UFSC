#include <iostream>
#include <vector>
#include <string>

const int C = 1e6;
int fw[C];

int pollen_quantity(int value) {
    std::string v = std::to_string(value);
    int sum = 0;
    for (int i = 0; i < v.size(); i++) {
        int val = v[i] - '0';
        sum += val;
    }
    return sum;
}

int main() {
    std::ios_base::sync_with_stdio(false);
    int n; int k;
    std::cin >> n >> k;

    int flower;
    for (int i = 0; i < n; i++) {
        std::cin >> flower;
        fw[flower]++;
    }


    int qtd = 0;
    int pollen = 0;
    for (int i = C; i >= 0; i--) {
        if (fw[i] != 0) {
            int nm = pollen_quantity(i);
            fw[i - nm]+= fw[i];
            qtd+=fw[i];
            if (qtd >= k) {
                pollen = nm;
                break;
            }
        }
    }
    std::cout << pollen << "\n";
    return 0;
}