#include <iostream>
#include <vector>

std::vector<long> obtained;

void withdraw(int x, std::vector<long> coins) {
    if (x == 0) return;

    long chosen = 0;
    for (long coin: coins) {
        if (coin <= x) {
            chosen = coin;
        }
    }
    obtained.push_back(chosen);
    withdraw((x-chosen), coins);
}


int main() {
    int t; std::cin >> t;
    while (t--) {
        int n; std::cin >> n;

        auto coins = std::vector<long>{};
        for (int i = 0; i < n; i++) {
            long coin; std::cin >> coin;
            coins.push_back(coin);
        }

        long total_sum = 1;
        for (int i = 1; i < n-1; i++) {
            if (total_sum + coins[i] < coins[i+1]) {
                total_sum += coins[i];
            }
        }

        obtained = std::vector<long>{};
        withdraw(total_sum, coins);

        std::cout << obtained.size()+1 << "\n";
    }
}