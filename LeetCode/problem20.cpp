#include <iostream>
#include <stack>
#include <string>

using namespace std;

class Solution {
    public:
        bool isValid(string s) {
            stack<char> st;
            for(char c:s){
                if(!st.empty()){
                    char last = st.top();
                    if(isPair(last,c)){
                        st.pop();
                        continue;
                    }
                }
                st.push(c);
            }  
            return st.empty();
        }
    private:
        bool isPair(char last, char c) {
            return (last == '(' && c == ')') ||
                   (last == '{' && c == '}') ||
                   (last == '[' && c == ']');
        }
};

int main() {
    Solution solution;
    string test = "{[()]}";
    if(solution.isValid(test)) {
        cout << "The string \"" << test << "\" is valid." << endl;
    } else {
        cout << "The string \"" << test << "\" is not valid." << endl;
    }
    return 0;
}