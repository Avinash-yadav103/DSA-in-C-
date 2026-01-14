class Solution {
public:
    bool isAnagram(string s, string t) {
        if(s.length() != t.length()) return false;
        set<char> c(s.begin(),s.end()); //entering string 1
        for(char l:c){ //checking string 2
            if(count(s.begin(),s.end(),l) != count(t.begin(), t.end(), l)){
                return false;
            }
        }
        return true;
    }
};