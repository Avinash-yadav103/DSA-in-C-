#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

class Solution {
public:
    string convertToTitle(int columnNumber) {
        string result;
        int n = columnNumber;
        while (n > 0) {
            n--; // Decrement n to handle 1-based indexing
            result += 'A' + n % 26;
            n = n / 26;
        }
        reverse(result.begin(), result.end());
        return result;
    }
};

int main() {
    Solution sol;
    int columnNumber;
    cout << "Enter column number: ";
    cin >> columnNumber;
    cout << "Excel column title: " << sol.convertToTitle(columnNumber) << endl;
    return 0;
}