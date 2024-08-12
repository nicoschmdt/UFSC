#include <iostream>
#include <array>

int mv;
std::array<int, 8> positions;


bool is_valid(int line, int column) {
    for (int c = 0; c < column; c++) {
        if (column - c == std::abs(positions[c] - line) || positions[c] == line) {
            return false;
        }
    }
    return true;
}

void solve(int column, std::array<int, 8> p, int moves) {
    if (column == 8) {
        mv = std::min(mv, moves);
        return;
    }
    for (int i = 0; i < 8; i++) {
        if (is_valid(i, column)) {
            positions[column] = i;
            if (p[column] != i) {
                solve(column+1, p, moves+1);
            } else {
                solve(column+1, p, moves);
            }
        }
    }
}

int main() {
    int position; int c = 1;
    while (std::cin >> position) {
        std::array<std::array<int, 8>, 8> board = {0};
        std::array<int, 8> initial_p = {position-1};
        for (int i = 1; i < 8; i++) {
            std::cin >> position;
            initial_p[i] = position-1;
        }

        mv = 8;
        solve(0, initial_p, 0);
        std::cout << "Case " << c << ": " << mv << "\n";
        c++;
    }
}
