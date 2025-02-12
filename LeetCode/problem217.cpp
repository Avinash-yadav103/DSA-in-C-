#include<iostream>
#include<vector>
#include<unordered_set>
using namespace std;

class Solution {
    public:
        bool containsDuplicate(vector<int>& nums) {
            unordered_set<int> num;
        
            for(int n:nums){
                num.insert(n);
            }
            if(num.size() == nums.size()) return false;

            return true;
        }
};

int main() {
    Solution solution;
    vector<int> nums = {1, 2, 3, 4, 5, 1}; // Example input
    bool result = solution.containsDuplicate(nums);
    cout << (result ? "Contains duplicates" : "No duplicates") << endl;
    return 0;
}