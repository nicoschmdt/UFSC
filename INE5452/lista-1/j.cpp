#include <bits/stdc++.h>

struct Card {
    int value;
    char key;
    char symbol;
};

using namespace std;

vector<Card> buildCards() {
    auto buildedCards = vector<Card>{};
    string chars = "AKQJT";

    for (auto i = 0; i<52; i++) {
        auto tmp = string{};
        std::cin>>tmp;
        int value = 10;
        if ((tmp[0] - '0') >= 2 || (tmp[0] - '0') <= 9) {
            value = tmp[0] - '0';
        }
        buildedCards.insert(buildedCards.begin(), Card{value, tmp[0], tmp[1]});
    }
    return buildedCards;
}


int main() {
    int currCase = 1;
    int casesQuantity;
    cin >> casesQuantity;
    cin.get();

    while (casesQuantity--) {
        int y = 0;
        auto hand = vector<Card>{};

        vector<Card> c = buildCards();

        for (int i = 0; i < 25; i++) {
            hand.insert(hand.begin(), c[i]);
        }
        c.erase(c.begin(),c.begin()+25);

        for (int i = 0; i < 3; i++) {
            int x = c[0].value;
            y += x;
            int qtdRemove = 10 - x;
            c.erase(c.begin(), c.begin()+qtdRemove+1);
        }

        for (int i = 0; i < hand.size(); i++) {
            c.insert(c.begin(), hand[i]);
        }

        int index = (c.size()) - y;
        Card answer = c[index];

        cout << "Case " << currCase << ": " << answer.key << answer.symbol << "\n";
        currCase++;
    }
    return 0;
}