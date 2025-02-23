#include <iostream>
#include <string>

using namespace std;

class Solution {
    public:
        int lengthOfLastWord(string s) {
            int count = 0;
            for(int i = s.size()-1; i >= 0; i--) {
                if(s[i] != ' ') {
                    count++;
                } else if(count > 0) {
                    return count;
                }
            }
            return count;
        }
};

int main() {
    Solution solution;
    string testString = "Hello World";
    int result = solution.lengthOfLastWord(testString);
    cout << "The length of the last word is: " << result << endl;
    return 0;
}
