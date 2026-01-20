class Solution {
public:
    bool isPowerOfTwo(int n) {

        for(int i =0;i<=30;i++){
            int ans = pow(2,i);
            if(ans==n){
                return true;
            }
        }
        return false;

    }
};
#include <iostream>
#include <cmath>
using namespace std;

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n;
    if (!(std::cin >> n)) return 0;

    Solution sol;
    std::cout << (sol.isPowerOfTwo(n) ? "true" : "false") << '\n';
    return 0;
}