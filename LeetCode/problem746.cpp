#include <iostream>
#include <vector>
#include <algorithm> // std::min

using namespace std;

class Solution {
public:
    int minCostClimbingStairs(vector<int>& cost) {
        int n = (int)cost.size();
        if (n == 0) return 0;
        if (n == 1) return cost[0];

        int value1 = cost[0];
        int value2 = cost[1];

        for (int i = 2; i < n; i++) {
            int sum = cost[i] + min(value1, value2);
            value1 = value2;
            value2 = sum;
        }
        return min(value1, value2);
    }
};

int main() {
    Solution s;

    // Example input; replace with your own or read from stdin
    vector<int> cost = {10, 15, 20};

    cout << s.minCostClimbingStairs(cost) << "\n";
    return 0;
}