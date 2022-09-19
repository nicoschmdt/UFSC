#include <stdlib.h>
#include <iostream>
#include <cmath>
#include <string>
#include <random>
#include <vector>

#include "DataAnalyserStudent.h"
#include "SolverStudent.h"

int main() {
    // auto solver = DataAnalyserStudent{};
    // auto n = 20;
    // auto k = 4;
    // auto avg = solver.movingAverage(n,k);

    // for (auto&& value: avg) {
    //     std::cout<<value<<", ";
    // }
    // std::cout<<"\n";
    // std::cout<<avg.size() << "\n";

    // teste de integral
    auto solver = SolverStudent{};
    solver.setMaxSteps(1e3);
    auto value = solver.integrate(0.0, 3.14159265358979323846, &seno);

    std::cout<<"value: "<<value<<"\n";
    // std::cout<<avg.size() << "\n";

}

double seno(double x) {
	return sin(x);
}