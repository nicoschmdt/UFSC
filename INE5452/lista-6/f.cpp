#include <iostream>
#include <tuple>
#include <map>

auto memo = std::map<std::tuple<int,int>, long>{};
int n;

long calculate(int exp_i, int exp_j) {
    if (memo.count(std::make_tuple(exp_i, exp_j)) > 0) {
        return memo[std::make_tuple(exp_i, exp_j)];
    }

    if(exp_i >= exp_j) {
        long first_result = 0;
        if (exp_i < n) {
            for (int k = exp_i+1; k <= n; k++) {
                first_result = std::max(calculate(k, 1) + calculate(k, exp_j), first_result);
            }
        }
        long second_result = 0;
        if (exp_j > 0) {
            int f_m = 0;
            for (int k = 1; k < exp_j; k++) {
                second_result = std::max(calculate(exp_i, k) + calculate(n, k), second_result);
            }
        }
        memo[std::make_tuple(exp_i, exp_j)] = first_result + second_result;
        return first_result + second_result;
    } else {
        long find_max = 0;
        for (int k = exp_i; k < exp_j; k++) {
            find_max = std::max(calculate(exp_i, k) + calculate(k+1, exp_j), find_max);
        }
        memo[std::make_tuple(exp_i, exp_j)] = find_max;
        return find_max;
    }
}

int main() {
    int an1;
    while (std::cin >> n >> an1) {
        memo.clear();
        memo[std::make_tuple(n, 1)] = an1;
        std::cout << calculate(1, n) << "\n";
    }
    return 0;
}