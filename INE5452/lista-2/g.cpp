#include <iostream>
#include <sstream>
#include <algorithm>
#include <vector>

struct Info {
    int id = 101;
    int solved = 0;
    int penalty = 0;
    int tries[10] = { 0 };
    int questions[10] = { 0 };
};

bool custom_compare (Info const& c1, Info const& c2) {
    if (c1.solved != c2.solved) return c1.solved > c2.solved;
    if (c1.penalty != c2.penalty) return c1.penalty < c2.penalty;
    return c1.id < c2.id;
}

int main() {
    int contestant; int problem; int time; char l;
    int caseNumber;
    scanf("%d\n", &caseNumber);

    for (int j = 0; j < caseNumber; j++) {
        int teams[101] = { 0 };
        
        std::vector<Info> subs(101);
        std::string line;
        while (std::getline(std::cin, line) && !line.empty()) {
            std::istringstream iss(line);
            iss >> contestant >> problem >> time >> l;
            
            if (teams[contestant] == 0) {
                teams[contestant] = 1;
                subs[contestant].id = contestant;
            }
            if (subs[contestant].questions[problem] != -1) {
                if (l == 'I') {
                    subs[contestant].tries[problem]++;
                } else if (l == 'C') {
                    int p = time + (subs[contestant].tries[problem]*20);
                    subs[contestant].penalty += p;
                    subs[contestant].solved += 1;
                    subs[contestant].questions[problem] = -1;
                }
            }
            
        }

        std::sort(subs.begin(), subs.end(), custom_compare);
        for (auto const& info: subs) {
            if (info.id != 101)
                printf("%d %d %d\n",info.id, info.solved, info.penalty);
        }
        if (j != caseNumber-1) printf("\n");
    }
    return 0;
}