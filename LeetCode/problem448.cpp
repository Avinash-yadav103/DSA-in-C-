class Solution {
public:
    vector<int> findDisappearedNumbers(vector<int>& nums) {
        // int n = nums.size();
        // vector<int> ans;
        // unordered_set<int> st(nums.begin(), nums.end());

        // for(int i =1;i<=n;i++){
        //     if(st.find(i) == st.end()){
        //         ans.push_back(i);
        //     }
        // }
        // return ans;

        vector<bool> a(nums.size(),false); //Initialize a vector with all false 
        vector<int> ans;
        for(int i=0;i<nums.size();i++){
            a[nums[i]-1]=true;
        }
        for(int i=0;i<nums.size();i++){
            if(a[i]==false){
                ans.push_back(i+1);
            }
        }
        
    
        return ans;
        
    }
};