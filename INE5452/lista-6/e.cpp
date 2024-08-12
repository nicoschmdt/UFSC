#include <iostream>
#include <tuple>
#include <map>
#include <vector>

typedef unsigned long long datatype;
datatype count;

auto memo = std::map<std::tuple<int,int>, int>{};

datatype trib(int n, unsigned int back) {
    datatype sum=0;
    count++;
    int count_before = count;
    if(n<=0) return 0;
    if(n==1) return 1;
    for(int i=1;i<=back;i++) {
        if (memo.count(std::make_tuple(n, back)) > 0) {
            count += memo[std::make_tuple(n, back)];
            return sum;
        }
        sum+=trib(n-i,back);
    }

    memo[std::make_tuple(n, back)] = (count - count_before);
    return sum;
}

int main() {
    memo.clear();
    int n; int back;
    int counter = 0;
    while(true) {
        std::cin >> n >> back;
        if (n > 60 || back > 60) break;

        count = 0;
        trib(n, back);
        std::cout << "Case " << ++counter << ": " << count << "\n";
    }
}