class Solution {
public:
    vector<vector<int>> fourSum(vector<int>& nums, int target) {
       vector<vector<int>>ans;
        int n=nums.size();
        sort(nums.begin(),nums.end());
        for(int i=0;i<n;i++){
            if(i>0&&nums[i]==nums[i-1])continue;
            for(int j=i+1;j<n;j++){
                if(j!=i+1&&nums[j]==nums[j-1])continue;
                int k=j+1;
                int r=n-1;
                while(k<r){
                    long long sum=nums[i];
                    sum+=nums[j];
                    sum+=nums[k];
                    sum+=nums[r];
                    if(sum==target){
                        vector<int>temp={nums[i],nums[j],nums[k],nums[r]};
                        ans.push_back(temp);
                        k++;r--;
                        while(k<r&&nums[k]==nums[k-1])k++;
                        while(k<r&&nums[r]==nums[r+1])r--;
                    }else if(sum<target)k++;
                    else r--;
                }
            }
        }return ans;
    }
};