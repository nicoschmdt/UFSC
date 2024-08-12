#include <iostream>
#include <vector>

struct Candidate {
    bool married = false;
    int age;
};


int main() {
    int bachelor_qtd; int spinster_qtd;
    int c = 1;
    while (true) {
        std::cin >> bachelor_qtd >> spinster_qtd;
        if (bachelor_qtd == 0 && spinster_qtd == 0) break;

        auto bachelors = std::vector<Candidate>{};
        int placeholder; 
        Candidate candidate;
        for (int i = 0; i < bachelor_qtd; i++) {
            std::cin >> placeholder;
            candidate.age = placeholder;
            bachelors.push_back(candidate);
        }

        auto spinsters = std::vector<Candidate>{};
        for (int i = 0; i < spinster_qtd; i++) {
            std::cin >> placeholder;
            candidate.age = placeholder;
            spinsters.push_back(candidate);
        }
        int left_bachelors = bachelor_qtd;
        for (int i = 0; i < bachelor_qtd; i++) {
            Candidate bachelor = bachelors[i];
            int s_selected;
            int age_diff = 60;
            for (int j = 0; j < spinster_qtd; j++) {
                if (!spinsters[j].married) {
                    int diff = std::abs(bachelor.age - spinsters[j].age);
                    if (diff < age_diff) {
                        age_diff = diff;
                        s_selected = j;
                    }
                }
            }

            if (age_diff != 60) {
                left_bachelors--;
                bachelor.married = true;
                spinsters[s_selected].married = true;
            }
        }

        std::cout << "Case " << c << ": " << left_bachelors;
        int youngest = 100;
        if (left_bachelors != 0) {
            for (int i = 0; i < bachelor_qtd; i++) {
                if (!bachelors[i].married) {
                    if (bachelors[i].age < youngest) {
                        youngest = bachelors[i].age;
                    }
                }
            }

            std::cout << " " << youngest;
        }
        std::cout  << std::endl;

        c++;
    }
    return 0;
}