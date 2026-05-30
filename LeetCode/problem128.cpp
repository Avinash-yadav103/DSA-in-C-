class Solution {
public:
    int longestConsecutive(vector<int>& nums) {
        //Using heapify approach
        if(nums.empty()){
            return 0;
        }

        priority_queue<int, vector<int>, greater<int>> pq;
        for(int num:nums){
            pq.push(num);
        }

        int longest = 1;
        int current = 1;

        int prev = pq.top();
        pq.pop();

        while(!pq.empty()){
            int curr = pq.top();
            pq.pop();

            if(curr == prev){
                continue;
            }
            if(curr == prev +1){
                current++;
            }
            else{
                longest = max(longest,current);
                current = 1;
            }

            prev = curr;
        }
        longest = max(longest,current);
        return longest;

        // Using Hashset Approach
    }
};