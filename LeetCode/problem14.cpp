class Solution {
public:
    string longestCommonPrefix(vector<string>& strs) {
        if(strs.empty()) return "";

        string res = strs[0];
        // int sequenceLength = 0;

        for(string s: strs)
            // string s = strs[i];
            while (s.find(res) != 0)
                res = res.substr(0, res.length() - 1);
        return res;
        

        // return res;

    }
};