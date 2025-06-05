#include<iostream>
#include<string>
#include<set>
using namespace std;
class Solution {
public:
    int lengthOfLongestSubstring(string s) {
        // char a = s[0];
        // string p;
        // int count = 0;
        // if(s.length()==1){
        //     return s[0];
        // }
        // for(int i=0;i<s.length();i++){
        //     if(!p.find(s[i])){
        //         p+=s[i];
        //         count++;
        //     }
        //     else count=0;

        // }
        // return count;
        set<char> sub;
        // int count;
        for(int i=0;i<s.length();i++){
            sub.insert(s[i]);
            // count++;
        }
        int a = sub.size();

        return a;
    }
};