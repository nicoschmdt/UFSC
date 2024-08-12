#include <iostream>
#include <numeric>
#include <vector>
#include <set>

int main() {
    int n; int t;
    while(std::cin >> n) {
        std::cin >> t;
        auto tracks = std::set<std::vector<int>>{};
        bool found = false;
        for (int i = 0; i < t; i++) {
            int d; std::cin >> d;
            if (found) continue;

            auto n_to_add = std::set<std::vector<int>>{};
            if (!tracks.empty()) {
                for (auto track: tracks) {
                    int sum = std::accumulate(track.begin(), track.end(), 0);
                    if (sum + d > n) continue;
                    if (sum+d == n && !found) {
                        for (int i = 0; i < track.size(); i++) {
                            std::cout << track[i] << " ";
                        }
                        std::cout << d << " sum:" << sum+d << "\n";
                        found = true;
                    }
                    auto to_add = std::vector<int>{};
                    for (int j = 0; j < track.size(); j++) {
                        to_add.push_back(track[j]);
                    }
                    to_add.push_back(d);
                    n_to_add.insert(to_add);
                }
            }
            n_to_add.insert(std::vector<int>{d});
            tracks.insert(n_to_add.begin(), n_to_add.end());
        }
        if (!found) {
            int prev = n;
            int sum_chosen = 0;
            std::vector<int> chosen;
            for (auto track: tracks) {
                int sum = std::accumulate(track.begin(), track.end(), 0);
                int diff = n - sum;
                if (diff >= 0 && diff < prev) {
                    prev = diff;
                    sum_chosen = sum;
                    chosen = track;
                }
            }
            for (int i = 0; i < chosen.size(); i++) {
                std::cout << chosen[i] << " ";
            }
            std::cout << "sum:" << sum_chosen << "\n";
        }
    }
    return 0;
}