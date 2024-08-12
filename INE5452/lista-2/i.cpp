#include <iostream>

int main() {
    // map(combination = popularity)
    int quantity;
    while(std::cin >> quantity && quantity != 0) {
        std::map<std::vector, int> combinations;
        for (int = 0; i < quantity; i++) {
            // each frosh
            int course;
            std::vector<int> courses = std::vector<int>{};
            for (int j = 0; j < 5; j++) {
                std::cin >> course;
                courses.push_back(course);
            }
            if (combinations.count(courses) > 0) {
                combinations[courses] += 1;
            } else {
                combinations[courses] = 1;
            }
            

        }
    }
    return 0;
}