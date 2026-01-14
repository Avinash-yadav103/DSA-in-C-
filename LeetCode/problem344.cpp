#include<iostream>
#include<vector>
using namespace std;

class Solution {
public:
    void reverseString(vector<char>& s) {
        int sk = 0;
        int e = s.size()-1;
        while(sk<e){
            swap(s[sk++],s[e--]);
        }
    }
};

int main(){
    return 0;
}