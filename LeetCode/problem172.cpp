class Solution {
public:
    int trailingZeroes(int n) {
        int zeroes = 0;
        while(n/5!=0){
            zeroes+=n/5;
            n/=5;
        }
        return zeroes;
    }
};
#include <iostream>
using namespace std;

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n;
    if (!(std::cin >> n)) return 0;

    Solution sol;
    std::cout << sol.trailingZeroes(n) << '\n';
    return 0;
}