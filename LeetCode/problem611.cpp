#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    int triangleNumber(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        int n = nums.size();
        int count = 0;
        
        for (int i = n - 1; i >= 2; i--) {
            int left = 0;
            int right = i - 1;
            
            while (left < right) {
                if (nums[left] + nums[right] > nums[i]) {
                    // All elements between left and right can form triangles with nums[i]
                    count += right - left;
                    right--;
                } else {
                    left++;
                }
            }
        }
        
        return count;
    }
};

int main() {
    Solution sol;
    
    // Example 1
    vector<int> nums1 = {2, 2, 3, 4};
    cout << "Example 1: " << sol.triangleNumber(nums1) << endl; // Expected output: 3
    
    // Example 2
    vector<int> nums2 = {4, 2, 3, 4};
    cout << "Example 2: " << sol.triangleNumber(nums2) << endl; // Expected output: 4
    
    return 0;
}