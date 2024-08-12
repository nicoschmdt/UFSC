#include <iostream>
#include <vector>
#include <queue>

int adj[10000][10000];
int visited[10000];


void search_bfs(int current, int answer, std::vector<int> buttons) {
    int cnt = 0;
    
    for (int v = 0; v < 10000; v++) {
        visited[v] = -1;
    }
    visited[current] = 0;

    std::queue<int> q;
    q.push(current);
    int cur;
    while (!q.empty()) {
        cur = q.front();
        q.pop();
        if (cur == answer) return;
        for (int i = 0; i < buttons.size(); i++) {
            int next = cur + buttons[i];
            if (next > 9999) {
                next = next%10000;
            }
            if (visited[next] == -1) {
                visited[next] = visited[cur] + 1;
                q.push(next);
            }
        }
    }
}

int main() {
    // l = lock code, u = unlock code, r = avail buttons
    int l; int u; int r;
    int c = 1;
    std::cin >> l >> u >> r;
    while (l != 0 || u != 0 || r != 0) {
        auto buttons = std::vector<int>{};
        for (int i = 0; i < r; i++) {
            int button; std::cin >> button;
            buttons.push_back(button);
        }

        search_bfs(l, u, buttons);
        std::cout << "Case " << c++ << ": ";
        if (visited[u] == -1) {
            std::cout << "Permanently Locked\n";
        } else {
            std::cout << visited[u] << "\n";
        }

        std::cin >> l >> u >> r;
    }
    return 0;
}