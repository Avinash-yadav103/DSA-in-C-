#include<iostream>
#include<map>
#include<unordered_map>
using namespace std;

int main(){
    // Creation
    unordered_map<string,int> m;

    // Insertion
    // 1
    pair<string,int> p = make_pair("Avinash",3);
    m.insert(p);

    // 2
    // pair,

    // 3
    m["mera"] = 2;  //Creation 
    m["mera"] = 1;  //Overlapping or Updation     

    // Searching 
    cout<<m["mera"]<<endl;
    cout<<m.at("Avinash")<<endl;


    return 0;
}