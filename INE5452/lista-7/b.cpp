#include <iostream>
#include <vector>
#include <sstream>
#include <stack>
#include <tuple>


int adj[99][99];
int visited[99][99];
int c_limit = 0;
int l_limit = 0;

std::vector<std::tuple<int, int>> get_neighbours(int l, int c) {
    int min_l = l ? l - 1 : l;
    int max_l = (l+1 >= l_limit) ? l_limit-1 : l+1;
    int min_c = c ? c - 1 : c;
    int max_c = (c+1 >= c_limit) ? c_limit-1 : c+1;

    auto neighbours = std::vector<std::tuple<int, int>>{};
    for (int c_line = min_l; c_line <= max_l; c_line++) {
        for (int c_column = min_c; c_column <= max_c; c_column++) {
            if (adj[c_line][c_column] == 1 && visited[c_line][c_column] != 1) {
                neighbours.push_back(std::make_tuple(c_line, c_column));
            }
        }
    }
    return neighbours;
}


int dfs(int line, int column) {
    auto stack = std::stack<std::tuple<int, int>>{};

    stack.push(std::make_tuple(line, column));

    int count = 0;
    while (!stack.empty()) {
        std::tuple<int, int> element = stack.top();
        int f = std::get<0>(element);
        int s = std::get<1>(element);
        if (visited[f][s] != 1) {
            count++;
            visited[f][s] = 1;
        }
        stack.pop();
        for (auto&& neighbour : get_neighbours(f, s)) {
            stack.push(std::make_tuple(std::get<0>(neighbour), std::get<1>(neighbour)));
        }
    }
    return count;    
}


void clean() {
    c_limit = 0;
    l_limit = 0;
    for (int i = 0; i < 99; i++) {
        for (int j = 0; j < 99; j++) {
            adj[i][j] = 0;
            visited[i][j] = 0;
        }
    }
}

void clean_visited() {
    for (int i = 0; i < 99; i++) {
        for (int j = 0; j < 99; j++) {
            visited[i][j] = 0;
        }
    }
}


int main() {
    int q; std::cin >> q;
    
    std::string line;
    std::getline(std::cin, line);
    std::getline(std::cin, line);
    int a = 0;
    while(q--) {
        if (a!=0) {
            std::cout << "\n";
        }
        a++;
        clean();
        while (std::getline(std::cin, line) && !line.empty()) {
            if (line[0] == 'W' || line[0] == 'L') {
                c_limit = line.size();
                for (int i = 0; i < line.size(); i++) {
                    if (line[i] == 'W') {
                        adj[l_limit][i] = 1;
                    }
                }
                l_limit++;
            } else {
                int first; int second;
                auto stream = std::istringstream{line};
                stream >> first >> second;

                std::cout << dfs(first-1, second-1) << "\n";
                clean_visited();
            }
        }
    }
}