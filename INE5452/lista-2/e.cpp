#include <iostream>
#include <stack>
#include <vector>

int main() {
    int quantity;
    while(std::cin >> quantity) {
        if (quantity == 0) break;
        
        int value;
        while (std::cin >> value) {
            if (value == 0) {
                break;
            }

            std::vector<int> expected = {value};
            for (int i = 0; i < quantity - 1; i++) {
                std::cin >> value;
                expected.push_back(value);
            }

            std::stack<int> initial;
            for (int i = quantity; i > 0; i--) {
                initial.push(i);
            }

            std::stack<int> station;
            std::stack<int> answer;

            bool valid = true;
            for (int i = 0; i < expected.size(); i++) {
                int expected_number = expected[i];
                if (!station.empty() && station.top() == expected_number) {
                    answer.push(station.top());
                    station.pop();
                } else {
                    while(!initial.empty() && (initial.top() != expected_number)) {
                        station.push(initial.top());
                        initial.pop();
                    }
                    if (!initial.empty()) {
                        answer.push(initial.top());
                        initial.pop();
                    } else {
                        valid = false;
                        break;
                    }
                }
            }
            if (station.empty()) std::cout << "Yes\n";
            else std::cout << "No\n";
        }
        std::cout << "\n";
    }
    return 0;
}