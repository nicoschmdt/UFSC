#include <iostream>
#include <string>
#include <ctime>
#include <vector>
#include <map>
#include <chrono>
#include <time.h>
#include <algorithm>

int main() {
    std::map<std::string, int> months = {{"January", 1},{"February", 2},{"March", 3},{"April", 4},{"May", 5},{"June", 6},{"July", 7},{"August", 8},{"September", 9},{"October", 10},{"November", 12},{"December", 12}};

    int t; std::cin >> t;
    for (int i = 0; i < t; i++) {
        std::vector<std::string> date;
        int year; std::cin >> year;
        std::string value; std::cin >> value;
        int days; std::cin >> days;
        value.erase(std::find(value.begin(), value.end(), '-'));
        value.erase(std::find(value.begin(), value.end(), '-'));

        std::tm tm;
        tm.tm_year = year;
        tm.tm_mon = months[value.substr(0, value.size()-2)];
        tm.tm_mday = std::stoi(value.substr(value.size()-2));

        std::cout << "year: " << year;
        std::cout << " month: " << tm.tm_mon;
        std::cout << " day: " << tm.tm_mday << "\n";

        // std::time_t tt = timegm(&tm);
        // std::chrono::system_clock::time_point init = std::chrono::system_clock::from_time_t(tt);

        // // auto current = std::chrono::sys_days{date[1]/day/year};
        std::mktime(&tm);
        std::cout << "current: " << std::asctime(&tm) << std::endl;
        // tm.tm_mday += days;

        // std::cout << "current: " << std::mktime(&tm) << std::endl;
        // auto test = std::chrono::sys_days{month/day/year} + std::chrono::duration{days};
        // std::cout << "Case " << ++i << ": " << test << "\n";
    }
    return 0;
}