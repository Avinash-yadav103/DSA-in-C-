class Solution {
public:
    vector<int> sortedSquares(vector<int>& nums) {
        int n = nums.size();
        vector<int> ans(n);

        int i = 0;
        int j = n - 1;
        int k = n - 1;

        while (i <= j) {
            int left = nums[i] * nums[i];
            int right = nums[j] * nums[j];

            if (left > right) {
                ans[k] = left;
                i++;
            } else {
                ans[k] = right;
                j--;
            }
            k--;
        }

        return ans;
    }
};