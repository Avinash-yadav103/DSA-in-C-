#include <bits/stdc++.h>
using namespace std;

class Solution {
public:
    int firstMissingPositive(vector<int>& nums) {
        int n = nums.size();
        for (int i = 0; i < n; i++) {
            while (nums[i] >= 1 && nums[i] <= n && nums[nums[i] - 1] != nums[i]) {
                swap(nums[i], nums[nums[i] - 1]);
            }
        }
        for (int i = 0; i < n; i++) {
            if (nums[i] != i + 1) return i + 1;
        }
        return n + 1;
    }
};

int main() {
    vector<int> nums;
    string line;
    getline(cin, line);
    stringstream ss(line);
    string token;
    while (ss >> token) {
        token.erase(remove(token.begin(), token.end(), ','), token.end());
        token.erase(remove(token.begin(), token.end(), '['), token.end());
        token.erase(remove(token.begin(), token.end(), ']'), token.end());
        if (!token.empty()) nums.push_back(stoi(token));
    }
    cout << Solution().firstMissingPositive(nums) << endl;
    return 0;
}
