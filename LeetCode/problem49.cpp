#include <iostream>
#include <vector>
#include <unordered_map>
#include <algorithm>
using namespace std;

class Solution {
public:
    vector<vector<string>> groupAnagrams(vector<string>& strs) {
        unordered_map<string, vector<string>> mp;  // key: sorted string, value: all anagrams
        
        cout << "Input strings:\n";
        for (string c : strs) cout << c << " ";
        cout << "\n\n";

        for (string c : strs) {
            string sortedStr = c;       // Make a copy of the string
            cout << "Original string: " << c << endl;

            sort(sortedStr.begin(), sortedStr.end());  // Sort characters to use as key
            cout << "Sorted string (key): " << sortedStr << endl;

            mp[sortedStr].push_back(c); // Push original string into map
            cout << "Map after inserting this string:\n";
            for (auto &pair : mp) {
                cout << "  Key: " << pair.first << " -> Values: ";
                for (auto &s : pair.second) cout << s << " ";
                cout << endl;
            }
            cout << "-------------------------\n";
        }
        
        // Prepare result
        vector<vector<string>> result;
        cout << "Collecting final result from map...\n";
        for (auto &pair : mp) {
            cout << "Key: " << pair.first << " -> Group: ";
            for (auto &s : pair.second) cout << s << " ";
            cout << endl;

            result.push_back(pair.second);  // push each group of anagrams
        }
        
        cout << "Final grouped anagrams:\n";
        for (auto &group : result) {
            for (auto &s : group) cout << s << " ";
            cout << endl;
        }

        return result;
    }
};

int main() {
    Solution sol;
    vector<string> strs = {"eat","tea","tan","ate","nat","bat"};
    sol.groupAnagrams(strs);
    return 0;
}
