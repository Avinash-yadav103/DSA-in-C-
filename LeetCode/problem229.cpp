#include <vector>
#include <unordered_map>

using namespace std;

class Solution {
    public:
        vector<int> majorityElement(vector<int>& nums) {
            int threshold = nums.size() / 3;
            unordered_map<int, int> mapi;
            vector<int> result;

            for(int num : nums) {
                mapi[num]++;
            }

            for(auto& pair : mapi) {
                if(pair.second > threshold) {
                    result.push_back(pair.first);
                }
            }

            return result;
        }
};