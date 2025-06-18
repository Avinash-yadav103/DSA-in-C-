#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <unordered_map>
using namespace std;

class Solution {
public:
    bool wordPattern(string pattern, string s) {
        vector<string> words;
        stringstream ss(s);
        string word;
        while (ss >> word) words.push_back(word);

        if (pattern.size() != words.size()) return false;

        unordered_map<char, string> charWord;
        unordered_map<string, char> wordChar;

        for (int i = 0; i < pattern.size(); i++) {
            char ch = pattern[i];
            string word = words[i];

            if (charWord.count(ch)) {
                if (charWord[ch] != word) return false;
            } else {
                if (wordChar.count(word) && wordChar[word] != ch) return false;
                charWord[ch] = word;
                wordChar[word] = ch;
            }
        }
        return true;
    }
};

int main() {
    Solution sol;
    string pattern, s;
    cout << "Enter pattern: ";
    cin >> pattern;
    cin.ignore();
    cout << "Enter string: ";
    getline(cin, s);

    bool result = sol.wordPattern(pattern, s);
    cout << (result ? "true" : "false") << endl;
    return 0;
}