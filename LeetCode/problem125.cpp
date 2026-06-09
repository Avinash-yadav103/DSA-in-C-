class Solution {
public:
    bool isPalindrome(string s) {
        string str = "";
        for(char ch: s){
            char c = tolower(ch);
             if ((c >= 'a' && c <= 'z') || (c >= '0' && c <= '9')){
                str.push_back(c);
            }
        }
        int len = str.length();
        int i=0;
        int j= len-1;
        while(i<j){
            if(str[i]!=str[j]){
                return false;
            }
            i++;
            j--;
        }
        return true;
    }
};