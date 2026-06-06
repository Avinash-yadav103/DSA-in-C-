class Solution {
public:
    vector<int> topKFrequent(vector<int>& nums, int k) {
        unordered_map<int,int> mp; //using unordered map to store freq
        for(int i:nums){
            mp[i]++;
        }

        // priority_queue<int,int> q;
        // for(auto i=0;i<)

        vector<pair<int,int>> vec;
        for(auto &[i,count]: mp){
            vec.push_back({count,i});
        }

        sort(vec.begin(),vec.end(), greater<>());
        vector<int> ans;
        for(int i =0;i<k;i++){
            ans.push_back(vec[i].second);
        }

        return ans;


    }
};