#include <iostream>
#include <string>
using namespace std;

class Solution {
public:
    int titleToNumber(string columnTitle) {
        int result = 0;
        for(char i: columnTitle){
            int p = i - 'A' + 1;
            result = result*26 + p;
        }
        return result;
    }
};

int main() {
    Solution sol;
    string columnTitle;
    cout << "Enter column title: ";
    cin >> columnTitle;
    int number = sol.titleToNumber(columnTitle);
    cout << "Column number: " << number << endl;
    return 0;
}