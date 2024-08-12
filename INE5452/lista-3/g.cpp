#include <iostream>


std::vector<std::vector<int>> results{};


int solve(int i) {
    
}


int main() {
    int t; int n;
    while (true) {
        std::cin >> t;
        std::cin >> n;
        if (t == 0 && n == 0) break;

        std::cout << "Sums of " << t << ":\n";
        std::vector<int> numbers{};
        for (int i = 0; i < n; i++) {
            int number; std::cin >> number;
            numbers.push_back(number);
        }

        if (solve(0)) {
            std::sort(results.begin(), results.end(), greater<int>());
            for (const auto& sums: results) {
                for(int i = 0; i < sums.size(); i++) {
                    std::cout << sums[i];
                    if (i < sums.size() - 1) {
                        std::cout << "+";
                    }
                }
                std::cout << "\n";
            }
        } else {
            std::cout << "NONE\n";
        }

    }
}