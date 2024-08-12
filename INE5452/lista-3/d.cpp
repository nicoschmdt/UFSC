#include <iostream>
#include <vector>

int eq1(int x, int y, int z) {
    return x + y + z;
}

int eq2(int x, int y, int z) {
    return x * y * z;
}

int eq3(int x, int y, int z) {
    return (x * x) + (y * y) + (z * z);
}

struct Solution {
    Solution(int xr, int yr, int zr) {
        x = xr;
        y = yr;
        z = zr;
    }
    int x;
    int y;
    int z;
};

int main() {
    int n; std::cin >> n;
    while (n--) {
        int a; int b; int c;
        std::cin >> a >> b >> c;
        auto solutions = std::vector<Solution>{};
        for (int x = -100; x < 100; x++) {
            for (int y = -100; y < 100; y++) {
                for (int z = -100; z < 100; z++) {
                    if (x == y || x == z || y == z) continue;
                    if (eq1(x,y,z) == a && eq2(x,y,z) == b && eq3(x,y,z) == c) {
                        solutions.push_back(Solution(x,y,z));
                    }
                }
            }
        }
        if (solutions.empty()) {
            std::cout << "No solution.\n";
        } else {
            Solution selected = solutions[0];
            for (int i = 1; i < solutions.size(); i++) {
                if (selected.x > solutions[i].x) {
                    selected = solutions[i];
                } else if (selected.x == solutions[i].x) {
                    if (selected.y > solutions[i].y) {
                        selected = solutions[i];
                    }
                }
            }
            std::cout << selected.x << " " << selected.y << " " << selected.z << "\n";
        }
    }
}