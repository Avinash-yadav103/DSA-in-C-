class Solution {
public:
    bool isSubsequence(string s, string t) {
        int j = 0;
        for(int i =0;i<t.length();i++){
            if(j<s.length() && s[j]==t[i]){
                j++;
                if(j==s.length()) return true;
            }
        }
        return s.length() == 0;
    }
};