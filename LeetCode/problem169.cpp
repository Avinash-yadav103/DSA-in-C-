#include <iostream>
#include <vector>
#include <unordered_map>

using namespace std;

class Solution {
public:
    int majorityElement(vector<int>& nums) {
        unordered_map<int, int> hash;
        int res = 0;
        int majority = 0;

        for (int n : nums) {
            hash[n] = 1 + hash[n];
            if (hash[n] > majority) {
                res = n;
                majority = hash[n];
            }
        }

        return res;
    }
};
// Existing Solution class code provided by user...
// (Assuming the user's class definition is above this block in the final file)

int main() {
    Solution sol;
    
    // Test case 1
    vector<int> nums1 = {3, 2, 3};
    cout << "Test Case 1: " << sol.majorityElement(nums1) << endl; // Expected: 3

    // Test case 2
    vector<int> nums2 = {2, 2, 1, 1, 1, 2, 2};
    cout << "Test Case 2: " << sol.majorityElement(nums2) << endl; // Expected: 2

    return 0;
}