class Solution {
public:

    bool isPalin(string &s, int start,int end){
        while(start<end){
            if(s[start] != s[end]){
                return false;
            }
            start++;
            end--;
        }
        return true;
    }

    bool validPalindrome(string s) {
        int start = 0;
        int end = s.length()-1;
        while(start<end){
            if(s[start]!=s[end]){
                return isPalin(s,start+1,end) || isPalin(s,start,end-1);
            }
            start++;
            end--;
        }
        return true;
    }
};