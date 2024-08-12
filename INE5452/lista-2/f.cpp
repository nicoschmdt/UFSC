#include <iostream>
#include <bitset>

int main() {
    long n; long m;
    long limit = 1000000;
    while(true) {
        std::cin >> n; std::cin >> m;
        if (n == 0 && m == 0) break;

        bool conflict = false;
        std::bitset<1000000> calendar{};
        //setting one time tasks
        long begin; long end;
        for (long i=0; i<n; i++) {
            std::cin >> begin; std::cin >> end;
            
            long initialIndex = begin;
            if (begin > 0) {
                initialIndex = begin - 1;
            }
            if ((calendar[initialIndex] == 1 && calendar[initialIndex+1] == 1) || calendar[end-1] == 1) {
                conflict = true;
                break;
            }
            
            for (long j=begin; j < end; j++) {
                calendar[j] = 1;
            }
        }

        //setting repeating time stasks
        long repetitionInterval;
        if (!conflict) {
            for (long i=0; i<m; i++) {
                std::cin >> begin; std::cin >> end;
                std::cin >>repetitionInterval;
                while (end < limit) {
                    long initialIndex;
                    if (begin > 0) {
                        initialIndex = begin - 1;
                    }
                    if (calendar[initialIndex] == 1 || calendar[end-1] == 1) {
                        conflict = true;
                        break;
                    }
                    
                    for (long j=begin; j < end; j++) {
                        calendar[j] = 1;
                    }

                    begin+=repetitionInterval;
                    end+=repetitionInterval;
                }
            }
        }

        if (conflict) {
            std::cout << "CONFLICT" << "\n";
        } else {
            std::cout << "NO CONFLICT" << "\n";
        }
    }
    return 0;
}