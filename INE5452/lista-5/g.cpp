#include <iostream>
#include <set>

int main() {
    int n;
    while (std::cin >> n && n!=0) {
        auto conjunto = std::set<int>{};

        int number;
        for (int i = 0; i < n; i++) {
            std::cin >> number;
            conjunto.insert(number);
        }
    }
}