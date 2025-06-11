#include<iostream>
#include<unordered_map>
#include<vector>
using namespace std;

int maximumFrequency(vector<int> &arr , int n){

    unordered_map<int , int> count;    
    for( int i=0;i<arr.size();i++){
        count[arr[i]]++;
    }
    int maxi= INT_MIN;
    int ans= INT_MIN;
    for(auto i:count){
        if(i.second>maxi){
            maxi = i.second;
            ans = i.first;
        }
    }
    return ans;
}

int main(){
    int n;
    cout << "Enter the number of elements: ";
    cin >> n;

    vector<int> arr(n);
    cout << "Enter the elements: ";
    for(int i = 0; i < n; i++) {
        cin >> arr[i];
    }

    int result = maximumFrequency(arr, n);
    cout << "Element with maximum frequency: " << result << endl;

    return 0;
}
