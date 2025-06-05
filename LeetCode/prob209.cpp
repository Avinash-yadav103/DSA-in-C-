
#include <iostream>
#include <vector>
#include <climits>
using namespace std;

class Solution {
public:
    int minSubArrayLen(int target, vector<int>& nums) {
        int left = 0;
        int right = 0;
        int current_sum = 0;
        int res = INT_MAX;

        for(int right = 0; right < nums.size(); right++) {
            current_sum += nums[right];
            while(current_sum >= target) {
                res = min(res, right - left + 1);
                current_sum -= nums[left];
                left++;
            }
        }
        return res == INT_MAX ? 0 : res;
    }
};

int main() {
    Solution sol;
    vector<int> nums = {2, 3, 1, 2, 4, 3};
    int target = 7;
    
    cout << "Minimum length of subarray with sum >= " << target << ": " 
            << sol.minSubArrayLen(target, nums) << endl;
    
    // Additional test case
    vector<int> nums2 = {1, 4, 4};
    target = 4;
    cout << "Minimum length of subarray with sum >= " << target << ": " 
            << sol.minSubArrayLen(target, nums2) << endl;
    
    return 0;
};