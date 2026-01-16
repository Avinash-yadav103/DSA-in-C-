#include <algorithm>
#include <iostream>
#include <string>

using namespace std;

class Solution {
public:
    bool canConstruct(string ransomNote, string magazine) {
        sort(ransomNote.begin(),ransomNote.end());
        sort(magazine.begin(),magazine.end());

        int i = 0;
        int j = 0;
        while(i<ransomNote.length() && j<magazine.length()){
            if(ransomNote[i]==magazine[j]){
                i++;j++;
            }
            else{
                j++;
            }
            
        }
        return i == ransomNote.length();
    }
};
int main() {
    std::string ransomNote, magazine;

    std::getline(std::cin, ransomNote);
    std::getline(std::cin, magazine);

    Solution sol;
    bool ok = sol.canConstruct(ransomNote, magazine);

    std::cout << (ok ? "true" : "false") << '\n';
    return 0;
}