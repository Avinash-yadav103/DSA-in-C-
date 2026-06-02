class Solution {
public:
    vector<int> findDuplicates(vector<int>& nums) {
        unordered_set<int> have;
        vector<int> ans;
        for(int num : nums){
            if(have.find(num) != have.end()){
                ans.push_back(num);
            }
            have.insert(num);
        }
        return ans;
    }
};