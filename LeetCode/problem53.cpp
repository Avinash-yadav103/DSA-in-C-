#include<iostream>
#include<vector>
using namespace std;


class Solution {
public:
    int maxSubArray(vector<int>& nums) {
        
        int sum = 0;
        int maxSum = INT_MIN;
        int n = nums.size();
        int sumIndex = 0;
        
        if(nums.size()==1){
            return nums[0];
        }
        
        for(int i=0;i<n;i++){
            sum = sum + nums[i];
            if(sum>maxSum){
                maxSum = sum;
                sumIndex = i;
            }
            if(sum < 0){
                sum = 0;
            }
        }
        
        int lastindex = sumIndex;
        int sumIndex2 = lastindex;
        sum = 0;
        for(int i=lastindex;i>=0;i--){
            sum += nums[i];
            if(sum == maxSum){
                sumIndex2 = i;
                break;
            }
        }
        
        return maxSum;
    }
};

int main() {
    Solution solution;
    
    // Test case 1: Basic example
    vector<int> nums1 = {-2, 1, -3, 4, -1, 2, 1, -5, 4};
    cout << "Test case 1: Maximum subarray sum = " << solution.maxSubArray(nums1) << endl;
    // Expected output: 6 (subarray [4, -1, 2, 1])
    
    // Test case 2: All negative numbers
    vector<int> nums2 = {-1, -2, -3, -4};
    cout << "Test case 2: Maximum subarray sum = " << solution.maxSubArray(nums2) << endl;
    // Expected output: -1
    
    // Test case 3: Single element
    vector<int> nums3 = {5};
    cout << "Test case 3: Maximum subarray sum = " << solution.maxSubArray(nums3) << endl;
    // Expected output: 5
    
    // Test case 4: All positive numbers
    vector<int> nums4 = {1, 2, 3, 4, 5};
    cout << "Test case 4: Maximum subarray sum = " << solution.maxSubArray(nums4) << endl;
    // Expected output: 15
    
    return 0;
}
