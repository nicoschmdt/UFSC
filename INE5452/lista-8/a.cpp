#include <iostream>
#include <vector>
#include <string>
#include <queue>
#include <map>
#include <sstream>

int adj[200][200];
auto dict = std::map<std::string, int>{};
int seq[200];


bool differ_only_one(std::string w1, std::string w2) {
    bool differ = false;
    if (std::abs((int)w1.size()-(int)w2.size()) > 1) return false;
    int s = w2.size();
    if (w1.size() > w2.size()) {
        s = w1.size();
    }

    for (int i = 0; i < s; i++) {
        if (w1[i] != w2[i]) {
            if (differ) {
                return false;
            }
            differ = true;
        }
    }
    if (differ) return true;
    return false;
}


void construct_graph(std::vector<std::string> words) {
    for (int i = 0; i < words.size(); i++) {
        for (int j = i+1; j < words.size(); j++) {
            if (differ_only_one(words[i], words[j])) {
                adj[i][j] = 1;
                adj[j][i] = 1;
            }
        }
    }
}

void clean_graph() {
    for (int i = 0; i < 200; i++) {
        for (int j = i+1; j < 200; j++) {
            adj[i][j] = 0;
            adj[j][i] = 0;
        }
    }
}


int search_bfs(std::string word, std::string expected, int limiter) {
    int index = dict[word];
    int expected_index = dict[expected];

    int cnt = 0;
    
    for (int v = 0; v < limiter; v++) {
        seq[v] = -1;
    }
    seq[index] = 0;

    std::queue<int> q;
    q.push(index);
    int cur_index;
    while (!q.empty()) {
        cur_index = q.front();
        if (cur_index == expected_index) return seq[cur_index];
        cnt = seq[cur_index] + 1;
        q.pop();
        for (int i = 0; i < limiter; i++) {
            if (adj[cur_index][i] == 1) {
                if (seq[i] == -1) {
                    seq[i] = cnt;
                    q.push(i);
                }
            }
        }
    }

    return 0;
}


int main() {
    int qtd; std::cin >> qtd;
    std::string w;
    std::getline(std::cin,w);
    for (int c = 1; c <= qtd; c++) {
        if (c!=1) std::cout << "\n";
        auto words = std::vector<std::string>{};

        std::string word;
        int num = 0;
        while (std::getline(std::cin, word) && word != "*") {
            words.push_back(word);
            dict[word] = num;
            num++;
        }

        construct_graph(words);

        
        std::string w1; std::string w2;
        while(true) {
            std::string line;
            std::getline(std::cin, line);
            if (line.size() == 0) break;

            std::istringstream stream{line};
            std::getline(stream, w1, ' ');
            std::getline(stream, w2);
            std::cout << w1 << " " << w2 << " " << search_bfs(w1, w2, words.size()) << "\n";
        }
        clean_graph();
    }
    return 0;
}