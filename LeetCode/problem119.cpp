#include<iostream>
#include<vector>
using namespace std;

class Solution {
public:
    vector<int> getRow(int rowIndex) {
        vector<vector<int>> res;
        for(int i = 0; i < rowIndex; i++) {
            vector<int> row;
            for(int j = 0; j <= i; j++) {
                if(j > 0 && j < i) {
                    row.push_back(res[i-1][j-1] + res[i-1][j]);
                } else {
                    row.push_back(1);
                }
            }
            res.push_back(row);
        }
        vector<int> newres;
        for(int j=0; j<=rowIndex; j++){
            newres.push_back(res[rowIndex-1][j]);
        }
        // newres.push_back()
        return newres;   
    }
};

class Solution {
public:
    vector<int> getotherRow(int rowIndex) {
        vector<vector<int>> s = generate(rowIndex + 1);
        return s[rowIndex];
    }

    vector<vector<int>> generate(int numRows) {
        vector<vector<int>> s;

        if (numRows >= 1) {
            vector<int> v {1};
            s.push_back(v);
        }
        if (numRows >= 2) {
            vector<int> v {1, 1};
            s.push_back(v);
        }
        for (int i = 3; i <= numRows; i++) {
            vector<int> v;
            v.push_back(1);
            
            for (int j = 1; j < i - 1; j++) {
                v.push_back(s[i - 2][j - 1] + s[i - 2][j]);
            }
            
            v.push_back(1);
            s.push_back(v);
        }

        return s;
    }
};