#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;


class Solution {
public:
    int twoCitySchedCost(vector<vector<int>>& costs) {
        int n = costs.size()/2;
        int total = 0;

        sort(costs.begin(), costs.end(),[](const vector<int> &a , const vector<int> &b){
            return (a[0]-a[1]< b[0]-b[1]);
        });

        for(int i=0;i<n;i++){
            total+= costs[i][0];
        }
        for(int i=n;i<2*n;i++){
            total+= costs[i][1];
        }

        return total;

    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int m;
    if (!(cin >> m)) return 0;

    vector<vector<int>> costs(m, vector<int>(2));
    for (int i = 0; i < m; ++i) {
        cin >> costs[i][0] >> costs[i][1];
    }

    Solution sol;
    cout << sol.twoCitySchedCost(costs) << '\n';
    return 0;
}