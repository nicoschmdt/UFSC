#include <iostream>
#include <vector>

std::vector<int> twin_primes;
long long is_prime[20000000];

void sieve_eratosthenes() {
    int limit = 20000000;
    int p = 2;
    while (p * p < limit) {
        if (is_prime[p] == 0) {
            for (int i = p*p; i < limit; i+=p) {
                is_prime[i] = 1;
            }
        }
        p++;
    }

    for (int i = 2; i < limit; i++) {
        if (is_prime[i] == 0 && is_prime[i+2] == 0) {
            twin_primes.push_back(i);
        }
    }
}


int main() {

    sieve_eratosthenes();

    int n;
    while (std::cin >> n) {
        auto number = twin_primes[n-1];
        std::cout << '(' << number << ", " << number+2 << ")\n";
    }

}