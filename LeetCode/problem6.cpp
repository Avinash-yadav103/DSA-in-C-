#include <iostream>
#include <string>
using namespace std;

class Solution {
public:
    string convert(string s, int n) {
        if(s.size() <= n || n == 1) return s;
        string ans = "";

        int a = 2*(n-1);
        int b = 0;

        for(int i=0; i<n; i++){
            int j=i;
            ans += s[j];
            while(j<s.size()){
                j += a;
                if(a && j<s.size()) ans += s[j];
                j += b;
                if(b && j<s.size()) ans += s[j];
            }
            a -= 2;
            b += 2;
        }

        return ans;
    }
};

int main() {
    Solution solution;
    string s = "PAYPALISHIRING";
    int n = 3;
    string result = solution.convert(s, n);
    cout << "Converted string: " << result << endl;
    return 0;
}