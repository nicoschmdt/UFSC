#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    long booksAvailable;
    while(std::cin >> booksAvailable) {
        auto prices = std::vector<long>{};
        for (int i = 0; i < booksAvailable; i++) {
            long price; std::cin >> price;
            prices.push_back(price);
        }
        long money; std::cin >> money;


        std::sort(prices.begin(), prices.end());

        auto cost = 1000001;
        int ci = -1; int cj = -1;

        for (int i = 0; i < prices.size(); i++) {
            if (prices[i] >= money) break;
            
            int needle = money - prices[i];
            if (std::binary_search(prices.begin(), prices.end(), needle)) {
                if (std::abs(prices[i] - needle) < cost) {
                    cost = std::abs(prices[i] - needle);
                    ci = prices[i];
                    cj = needle;
                    if (prices[i] > needle) {
                        ci = needle;
                        cj = prices[i];
                    }
                }
            }
        }

        std::cout << "Peter should buy books whose prices are " << ci << " and " << cj << ".\n\n";
    }
    return 0;
}