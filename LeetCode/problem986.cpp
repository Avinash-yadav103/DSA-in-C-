class Solution {
public:
    vector<vector<int>> intervalIntersection(vector<vector<int>>& firstList, vector<vector<int>>& secondList) {
        int m = firstList.size();
        int n = secondList.size();
        int first = 0;
        int second = 0;
        vector<vector<int>> ans;
        while(first< m && second< n){
            vector<int> &a = firstList[first];
            vector<int> &b = secondList[second];

            int start = max(a[0],b[0]); 
            int end = min(a[1],b[1]);

            if(start<=end){
                ans.push_back({start,end});
            }
            if(a[1]<b[1]){
                first++;
            }
            else second++;
        }
        return ans;
    }
};