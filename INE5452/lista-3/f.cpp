#include <iostream>
#include <vector>

struct Piece {
    Piece(int a, int b, bool placed) {
        sideA = a;
        sideB = b;
        placed = placed;
    }

    Piece() {
        sideA = -1;
        sideB = -1;
        placed = false;
    }

    void reverse() {
        int aux = sideA;
        sideA = sideB;
        sideB = aux;
    }
    int sideA;
    int sideB;
    bool placed = false;
};

Piece table [16];
int limit;

bool place(std::vector<Piece> &pieces, int index) {
    if (index == limit - 1) return true;

    Piece before = table[index - 1];
    std::cout << "piece before: " << "<"<< before.sideA << "|" << before.sideB << ">\n";
    bool worked = false;
    
    std::cout << "index: " << index << "\n";
    for (int i = 0; i < limit; i++) {
        std::cout << " <"<< table[i].sideA << "|" << table[i].sideB << "> ";
    }
    std::cout << "\n";

    for (int i = 0; i < pieces.size(); i++) {
        Piece piece = pieces[i];
        std::cout << "piece: " << "<"<< piece.sideA << "|" << piece.sideB << ">\n";
        std::cout << "placed: " << piece.placed << "\n";
        if (piece.placed) {
            std::cout << "já posicionada\n";
            continue;
        }
        if (piece.sideA == before.sideB) {
            table[index] = piece;
            table[index].placed = true;
            worked = place(pieces, index+1);
        } else if (piece.sideB == before.sideB) {
            table[index] = piece;
            table[index].reverse();
            table[index].placed = true;
            worked = place(pieces, index+1);
        }

        if (!worked) {
            table[index].placed = false;
        }
    }
    return false;
}


int main() {
    int n; int m;
    while (std::cin >> n && n != 0) {
        std::cin >> m;
        limit = n + 2;

        int a; int b;
        std::cin >> a >> b;
        table[0] = Piece(a,b, true);
        std::cin >> a >> b;
        table[n+1] = Piece(a,b, true);

        auto pieces = std::vector<Piece>{};
        for (int i = 0; i < m; i++) {
            std::cin >> a >> b;
            pieces.push_back(Piece(a, b, false));
        }

        if (place(pieces, 1)) {
            std::cout << "YES\n";
        } else {
            std::cout << "NO\n";
        }
    }
    return 0;
}