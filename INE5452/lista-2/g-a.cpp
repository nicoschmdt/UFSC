#include <iostream>
#include <map>
#include <algorithm>
#include <vector>

using namespace std;

struct contestant 
{
    int id = 101;
    int n_probl_solved = 0;
    int penalties = 0;
    map<int, int> problem_solving_attemps;
};

bool sort_func(const contestant &a, const contestant &b) 
{
    if (a.n_probl_solved != b.n_probl_solved) 
        return a.n_probl_solved > b.n_probl_solved;
    if (a.penalties != b.penalties) 
        return a.penalties < b.penalties;
    return a.id < b.id;
}

int main() 
{
    int temp3 = 0;
    int n, id, probl, time;
    char status;
    cin >> n;
    cin.ignore();
    cin.ignore();

    for (int i = 0; i < n; i++) 
    {
        int n_contestants = 0;
        vector<contestant> contestants(101);
        string line;
        while (getline(cin, line) && !line.empty()) 
        {
            sscanf(line.c_str(), "%d %d %d %c", &id, &probl, &time, &status);
            if (contestants[id].id == 101) 
            {
                n_contestants++;
                contestants[id].id = id;
            }
            if (status == 'C') 
            {
                if (contestants[id].problem_solving_attemps[probl] != -1) 
                {
                    contestants[id].n_probl_solved += 1;
                    contestants[id].penalties += 20 * contestants[id].problem_solving_attemps[probl];
                    contestants[id].penalties += time;
                    contestants[id].problem_solving_attemps[probl] = -1;
                }
            } 
            else if (status == 'I') 
            {
                if (contestants[id].problem_solving_attemps[probl] != -1)
                    contestants[id].problem_solving_attemps[probl] += 1;
            }
        }
        partial_sort(contestants.begin(), contestants.begin() + n_contestants, contestants.end(), sort_func);
        for (contestant &c : contestants) 
        {
            if (c.id == 101) 
                break;
            cout << c.id << " " << c.n_probl_solved << " " << c.penalties << endl;
        }
        if (i != n - 1) 
            cout << endl;
    }
    return 0;
}