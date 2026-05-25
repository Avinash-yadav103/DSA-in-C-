class Solution {
public:
    vector<int> productExceptSelf(vector<int>& nums) {
        
        int size = nums.size();
        int product = 1;
        int zeroCount = 0;

        // Calculate product of non-zero elements
        for(int i = 0; i < size; i++) {
            if(nums[i] == 0) {
                zeroCount++;
            } else {
                product *= nums[i];
            }
        }

        vector<int> pro(size);

        for(int i = 0; i < size; i++) {

            // More than one zero
            if(zeroCount > 1) {
                pro[i] = 0;
            }

            // Exactly one zero
            else if(zeroCount == 1) {

                if(nums[i] == 0)
                    pro[i] = product;
                else
                    pro[i] = 0;
            }

            // No zero
            else {
                pro[i] = product / nums[i];
            }
        }

        return pro;
    }
};