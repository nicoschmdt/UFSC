#include <iostream>
#include <vector>

int streak(std::vector<int> numbers) {
    auto current = 0;
    auto maximum = 0;
    for(int i = 0; i < numbers.size(); i++) {
        if (current + numbers[i] > 0) {
            current += numbers[i];

            if (current > maximum) {
                maximum = current;
            }
        } else {
            current = 0;
        }
    }
    return maximum;
}

int main() {
    int n = -1;
    while (true) {
        std::cin >> n;
        if (n == 0) break;
        auto numbers = std::vector<int>{};
        for (int i = 0; i < n; i++) {
            int number; std::cin >> number;
            numbers.push_back(number);
        }

        int result = streak(numbers);
        if (result == 0) {
            std::cout << "Losing streak.\n";
        } else {
            std::cout << "The maximum winning streak is " << result << ".\n";
        }
    }
}