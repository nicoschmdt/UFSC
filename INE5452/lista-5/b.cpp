#include <algorithm>
#include <iostream>
#include <vector>
#include <sstream>


int combine(std::vector<int> morning, std::vector<int> evening, int n, int d, int r) {
    int overtime = 0;

    std::sort(morning.begin(), morning.end());
    std::sort(evening.begin(), evening.end(), std::greater<int>());

    for (int i = 0; i < n; i++) {
        if (morning[i] + evening[i] > d) {
            overtime += morning[i] + evening[i] - d;
        }
    }


    return overtime * r;
}


int main() {
    int n; int d; int r;
    while(true) {
        std::cin >> n >> d >> r;
        if (n == 0 && d == 0 && r == 0) break;

        auto morning_routes = std::vector<int>{};
        int distance;
        for (int i = 0; i < n; i++) {
            std::cin >> distance;
            morning_routes.push_back(distance);
        }

        auto evening_routes = std::vector<int>{};
        for (int i = 0; i < n; i++) {
            std::cin >> distance;
            evening_routes.push_back(distance);
        }
        std::cout << combine(morning_routes, evening_routes, n, d, r) << std::endl;
    }
    return 0;
}