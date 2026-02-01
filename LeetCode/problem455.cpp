#include <iostream>
#include <vector>
#include <algorithm>

class Solution {
public:
    int findContentChildren(vector<int>& g, vector<int>& s) {
        sort(g.begin(),g.end());
        sort(s.begin(),s.end());
        int res=0,i=0;
        for(int j=0;j<g.size();j++)
        {
            while(i<s.size() && s[i]<g[j])
            {
                i++;
            }
            if(i == s.size())
            {
                return res;
            }
            res++;
            i++;
        }
        return res;
    }
};


int main() {
    std::vector<int> g = {1, 2, 3};
    std::vector<int> s = {1, 1};

    Solution sol;
    std::cout << sol.findContentChildren(g, s) << "\n";

    return 0;
}