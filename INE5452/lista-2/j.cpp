#include <iostream>
#include <iomanip>
#include <set>
#include <map>

int main() {
    std::cout << std::fixed << std::setprecision(6);
    long case_quantity;
    std::cin >> case_quantity;
    long case_count = 0;
    while (case_quantity--) {
        std::map<long, std::set<long>> stamp_info{};
        long friend_quantity; std::cin >> friend_quantity;
        for (long friend_id = 0; friend_id < friend_quantity; friend_id++) {
            long stampsQuantity; std::cin >> stampsQuantity;
            for (long i = 0; i < stampsQuantity; i++) {
                long stamp; std::cin >> stamp;
                if(stamp_info.count(stamp) == 0) {
                    stamp_info[stamp] = {friend_id};
                } else {
                    stamp_info[stamp].insert(friend_id);
                }
            }
        }

        std::map<long, long> unique{};
        long unique_quantity = 0;
        for (const auto& [key, set] : stamp_info) {
            if (set.size() == 1) {
                unique_quantity++;
                unique[*set.begin()]++;
            }
        }

        std::cout << "Case " << ++case_count << ": ";
        for (int i=0; i<unique.size(); i++) {
        // for (const auto& [key, qtd] : unique) {
            double result = (double) unique[i] / unique_quantity * 100.0;
            std::cout << result << "%";
            if (i != unique.size() - 1) {
                std::cout << " ";
            } else {
                std::cout << "\n";
            }
        }
    }
    return 0;
}