#include <iostream>
#include <vector>

struct Field {
    bool has_scarecrown = false;
    bool infertile = false;
    bool covered = false;
};

int main() {
    int t; std::cin >> t;
    for (int case_n = 1; case_n <= t; case_n++) {
        int n; std::cin >> n;
        auto sequences = std::vector<Field>{};
        char f;
        for (int i = 0; i < n; i++) {
            std::cin >> f;
            Field field;
            if (f == '#') {
                field.infertile = true;
            }
            sequences.push_back(field);

        }

        int need_protection = 0;
        int needed = 0;
        for (int i = 0; i < sequences.size(); i++) {
            if (!sequences[i].infertile && !sequences[i].covered) {
                need_protection++;
            } else if ((sequences[i].infertile) && need_protection != 0) {
                int index = i;
                if (need_protection == 2) {
                    index = i - 1;
                }
                sequences[index].has_scarecrown = true;
                sequences[index].covered = true;
                if (index > 0)
                    sequences[index-1].covered = true;
                needed++;
                need_protection = 0;

                if ((index+1) < sequences.size()) {
                    sequences[index+1].covered = true;
                }
            }

            if (need_protection == 3) {
                sequences[i-1].has_scarecrown = true;
                sequences[i-1].covered = true;
                sequences[i].covered = true;
                sequences[i-2].covered = true;
                needed++;
                need_protection = 0;
            }
        }
        if (need_protection != 0) {
            needed++;
        }
        std::cout << "Case " << case_n << ": " << needed << std::endl;
    }
}