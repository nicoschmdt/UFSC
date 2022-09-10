#include <iostream>
#include "DataAnalyserStudent.h"

int main() {
    auto solver = DataAnalyserStudent{};
    auto n = 20;
    auto k = 4;
    auto avg = solver.movingAverage(n,k);

    for (auto&& value: avg) {
        std::cout<<value<<", ";
    }
    std::cout<<"\n";
    std::cout<<avg.size() << "\n";
}