#include<iostream>
#include<vector>
#include<unordered_map>
using namespace std;
class Solution {
public:
    int subarraySum(vector<int>& nums, int k) {
        
        // int count =0;
        // int n = nums.size();
        // for(int i =0;i<n;i++){
        //     int current_sum=nums[0];
        //     if(nums[i]==k){
        //         count++;
        //         // continue;
        //     }
        //     current_sum = max(current_sum, current_sum+nums[i]);
        //     // max_sum = max(current_sum, max_sum);
        //     if(current_sum== k){
        //         count++;
        //         continue;
        //     }
        //     if(current_sum>k){
        //         current_sum=0;
        //     }
        // }

        // return count;

        int n = nums.size();
        unordered_map<int, int> mpp;
        int preSum = 0, count = 0;

        mpp[0] = 1;

        for (int i = 0; i < n; i++) {
            preSum += nums[i];
            int remove = preSum - k;
            count += mpp[remove];
            mpp[preSum]++;
        }

        return count;

    }
};


int main() {
    // Create an instance of the Solution class
    Solution solution;
    
    // Example test cases
    vector<int> nums1 = {1, 1, 1};
    int k1 = 2;
    cout << "Example 1: Input [1,1,1], k=2" << endl;
    cout << "Output: " << solution.subarraySum(nums1, k1) << endl; // Should output 2
    
    vector<int> nums2 = {1, 2, 3};
    int k2 = 3;
    cout << "Example 2: Input [1,2,3], k=3" << endl;
    cout << "Output: " << solution.subarraySum(nums2, k2) << endl; // Should output 2
    
    vector<int> nums3 = {-1, -1, 1};
    int k3 = 0;
    cout << "Example 3: Input [-1,-1,1], k=0" << endl;
    cout << "Output: " << solution.subarraySum(nums3, k3) << endl; // Should output 1
    
    return 0;
}
