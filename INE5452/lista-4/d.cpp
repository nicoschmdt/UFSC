#include <iostream>
#include <cmath>
#include <iomanip>

double p, q, r, s, t, u;

double func(double x) {
    return p * std::exp(-x) + (q * std::sin(x)) + (r * std::cos(x)) + (s * std::tan(x)) + t * std::pow(x,2) + u;
}

double bisection(double a, double b) {
    double c;
    while ((b-a) >= (1e-9)) {
        c = (a+b)/2;

        if (func(c)*func(a) <= 0) {
            b = c;
        } else {
            a = c;
        }
    }
    return c;
}

int main() {
    std::cout << std::fixed << std::setprecision(4);
    while (std::cin >> p) {
        std::cin >> q >> r >> s >> t >> u;
        if (func(0) * func(1) > 0) {
            std::cout << "No solution\n";
        } else {
            std::cout << bisection(0.0, 1.0) << "\n";
        }
    }
    return 0;
}