#include <iostream>
#include <sstream>

int critic[99];
int blocks[99][99];

void clean() {
    for (int i = 0; i < 99; i++) {
        critic[i] = 0;
        for (int j = i; j < 99; j++) {
            blocks[i][j] = 0;
            blocks[j][i] = 0;
        }
    }
}

void print(int n) {
    for (int i = 0; i <= n; i++) {
        for (int j = 0; j <= n; j++) {
            std::cout << blocks[i][j] << " ";
        }
        std::cout << "\n";
    }
    for (int i = 0; i <= n; i++) {
        std::cout << critic[i] << " ";
    }
    std::cout << "\n";
}

int set_critic(int n) {
    for (int i = 0; i <= n; i++) {
        int connections = 0;
        int critic_c = 0;
        for (int j = 0; j <= n; j++) {
            if (blocks[i][j] == 1) {
                if (connections == 0) {
                    critic_c = j;
                }
                connections++;
            }
        }
        if (connections == 1) {
            critic[critic_c] = 1;
        }
    }
    print(n);

    int p = 0;
    for (int a = 0; a <= n; a++) {
        if (critic[a] == 1) {
            p++;
        }
    }
    return p;
}

int main() {
    int n; std::cin >> n;
    while(n) {
        std::cout << "n: " << n << "\n";
        std::string line;
        while (std::getline(std::cin, line)) {
            auto stream = std::istringstream{line};
            int i; stream >> i;
            if (i==0) break;
            for (int j = 1; j < (line.size()+1)/2; j++) {
                int number; stream >> number;
                blocks[i][number] = 1;
                blocks[number][i] = 1;
            }
        }

        std::cout << set_critic(n) << "\n";
        clean();
        std::cin >> n;
    }
}