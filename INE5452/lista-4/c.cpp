#include <iostream>
#include <vector>
#include <set>


int binary_search(int min, int max, int higher_b, int diag_jump, std::vector<int> crops) {
    int med = 
    if ()
}


void find_square(std::vector<int> crops, int line_size) {
    int lower_b; int higher_b;
    std::cin >> lower_b >> higher_b;

    auto size_found = std::set<int>{0};
    for (int i = 0; i < crops.size(); i++) {
        if (crops[i] < lower_b || crops[i] > higher_b) continue;
        
        //
        binary_search(i, ())
        //

        int curr_ls = 1;
        int diag = i;
        while (diag + line_size + 1 < crops.size() 
                && crops[diag+line_size+1] <= higher_b
                && (i%line_size < (diag+line_size+1)%line_size)) {
            curr_ls += 1;
            diag += line_size + 1;
        }
        size_found.insert(curr_ls);
    }
    std::cout << *size_found.rbegin() << "\n";
}



int main() {
    int line; int column;
    while (std::cin >> line && line != 0) {
        std::cin >> column;

        auto crops = std::vector<int>{};
        for (int i = 0; i < line*column; i++) {
            int value; std::cin >> value;
            crops.push_back(value);
        }

        int case_qtd; std::cin >> case_qtd;
        while(case_qtd--) {
            find_square(crops, line);
        }
        std::cout << "-\n";
    }
    return 0;
}