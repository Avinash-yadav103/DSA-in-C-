#include<iostream>
#include<string>
using namespace std;

class Solution {
public:
    string addBinary(string a, string b) {
        int m = a.size()-1;
        int n = b.size()-1;

        int carry = 0;
        while(m>=0 || n>=0 || carry ){
            if(m>=0){
                
            }
            if(n>=0){
                
            }
        }

    }
};
int main() {
    Solution solution;
    string a = "1010";
    string b = "1011";
    cout << "Result: " << solution.addBinary(a, b) << endl;
    return 0;
}