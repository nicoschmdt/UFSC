#include <bits/stdc++.h>
#include <iostream>
#include <sstream>
#include <vector>
#include <queue>
#include <string>

int LIMIT;
int capacity[100][100];


std::vector<int> bfs(int s, int t, int parent[]) {
    int visited[LIMIT+1] = { 0 };

    std::queue<int> q;
    q.push(s);
    visited[s] = 1;

    while (!q.empty()) {
        int u = q.front();
        q.pop();

        for (int i = 1; i <= LIMIT; i++) {
            if (capacity[u][i] > 0 && visited[i] == 0) {
                visited[i] = 1
                q.push(i);
                parent[i] = u;
            }
        }

        // if (u == t) {
        //     auto path = std::vector<int>{};
        //     while (true) {
        //         path.push_back(u);
        //         if (u == s) break;
        //         u = parent[u];
        //     }
        //     return path;
        // }

        // for (int i = 0; i <= LIMIT; i++) {
        //     if (capacity[u][i] > 0 && visited[i] == 0) {
        //         q.push(i);
        //         visited[i] = 1;
        //         parent[i] = u;
        //     }
        // }
    }
    return std::vector<int>{};
}


int edmonds_karp(int s, int t) {
    int parent[LIMIT] = { 0 };
    int max_flow = 0;
    
    auto path = bfs(s, t, parent);
    while(!path.empty()) {
        int path_flow = 1001;
        for (int v = t; v != s; v = parent[v]) {
            path_flow = std::min(path_flow, capacity[parent[v]][v]);
        }
        
        for (int vertex = t; vertex != s; vertex = parent[vertex]) {
            capacity[parent[vertex]][vertex] -= path_flow;
            capacity[vertex][parent[vertex]] += path_flow;
        }
        max_flow += path_flow;
        parent[LIMIT] = { 0 };
        path = bfs(s, t, parent);
    }
    return max_flow;
}


int main() {
    std::ios_base::sync_with_stdio(false);
    int network = 0;
    int s; int t; int c;

    while (std::cin >> LIMIT && LIMIT != 0) {
        if (network) std::cout << "\n";
        std::cout << "Network " << ++network << "\n";

        int s; int t; int c;
        std::cin >> s >> t >> c;
        for(int i = 0; i < c; i++) {
            int n1; int n2; int cap;
            std::cin >> n1 >> n2 >> cap;
            capacity[n1][n2] += cap;
            capacity[n2][n1] += cap;
        }

        std::cout << "The bandwidth is " << edmonds_karp(s, t) << ".\n";
    }
    return 0;
}