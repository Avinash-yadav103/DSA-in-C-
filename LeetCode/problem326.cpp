#include <iostream>

class Solution {
public:
    bool isPowerOfThree(int n) {
        if (n <= 0) return false;
        while (n % 3 == 0) {
            n /= 3;
        }
        return n == 1;
    }
};

int main() {
    Solution sol;

    int n;
    std::cin >> n;

    std::cout << (sol.isPowerOfThree(n) ? "true" : "false") << '\n';
    return 0;
}