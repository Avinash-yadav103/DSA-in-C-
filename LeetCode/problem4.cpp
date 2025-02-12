#include<iostream>
#include<vector>
using namespace std;

class Solution {
    public:
        double findMedianSortedArrays(vector<int>& nums1, vector<int>& nums2) {
            vector<int> nums;
            int m = nums1.size()-1;
            int n = nums2.size()-1;
            int i = 0, j = 0;
            while(i <= m && j <= n){
                if(nums1[i] < nums2[j]){
                    nums.push_back(nums1[i++]);
                }
                else{
                    nums.push_back(nums2[j++]);
                }
            }
            while(i <= m){
                nums.push_back(nums1[i++]);
            }
            while(j <= n){
                nums.push_back(nums2[j++]);
            }
    
            int totalSize = nums.size();
            if(totalSize % 2 == 1){
                return nums[totalSize / 2];
            }
            else{
                return (nums[totalSize / 2 - 1] + nums[totalSize / 2]) / 2.0;
            }
        }
};

int main() {
    Solution solution;
    vector<int> nums1 = {1, 3};
    vector<int> nums2 = {2};
    double median = solution.findMedianSortedArrays(nums1, nums2);
    cout << "The median is: " << median << endl;
    return 0;
}