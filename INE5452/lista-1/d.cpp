#include <iostream>
#include <sstream>
#include <string>
#include <cstring>
#include <algorithm>


bool isPalindrome(std::string phrase) {
    for (auto i = 0; i < phrase.size()/2; i++) {
        if (std::tolower(phrase[i]) != std::tolower(phrase[phrase.size()-i-1])) {
            return false;
        }
    }
    return true;
}

int main () {
    auto phrase = std::string{};
    char chars[] = ".,!? ";

    while (true) {
        std::getline(std::cin, phrase);
        //get phrase
        if (phrase == "DONE") {
            break;
        }
        
        // clean
        for (auto i = 0; i < phrase.size(); i++) {
            phrase.erase(std::remove(phrase.begin(), phrase.end(), chars[i]), phrase.end());
        }

        if (isPalindrome(phrase)) {
            std::cout << "You won't be eaten!\n";
        } else {
            std::cout << "Uh oh..\n";
        }
    }

    return 0;
}