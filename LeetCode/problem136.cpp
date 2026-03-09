class Solution {
public:
    int singleNumber(vector<int>& nums) {
        int unique = 0;
        // // int current;
        int n = nums.size();
        // if (n==1) return nums[0];
        for(int i=0;i<n;i++){
            unique ^= nums[i]; 
        }
        return unique;
        // int n = nums.size();
        // sort(nums.begin(), nums.end());
        // for (int i = 0; i < n - 1; i += 2) {
        //     if (nums[i] != nums[i + 1]) return nums[i];
        // }
        // return nums[n - 1];
    }
};