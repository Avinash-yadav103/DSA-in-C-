#include<iostream>
#include<vector>
using namespace std;

void reverseWords(vector<char> &s){
    for(int i;i<s.size();i++){
        if(s[i]==' '){
            cout<<"Hello";
        }
    }
}

int main(){
    
    vector<char> hello = {'H', 'e', 'l', 'l', 'o', ' ', 't', 'h', 'e', 'r', 'e', ' ', 't', 'h', 'i', 's', ' ', 'i', 's', ' ', 'm', 'e'};

    // for(int i;i<hello.size();i++){
    //     cin>>hello[i];
    // }
    reverseWords(hello);

    return 0;
}