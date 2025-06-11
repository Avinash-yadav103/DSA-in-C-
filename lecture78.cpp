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

    // cout<< m.at('unkownKey')<<endl; //Yaha error dega kyu milaga ni
    cout<< m["unknownKey"] <<endl; //nhi bna dega m ke corresponding
    cout<< m.at("unknownKey")<<endl;

    cout<<m.size()<<endl;

    cout<< m.count("bro")<<endl;
    // if absent gives 0
    // if present gives 1

    m.erase("mera");
    cout<< "Size:"<<m.size()<<endl;

    //Traversal
    for(auto i:m){
        cout<<i.first<<" "<<i.second;
        cout<<endl;
    }
    cout<<endl;

    //iterator
    unordered_map<string,int>:: iterator it = m.begin();
    while(it!= m.end()){
        cout<< it->first<< " "<<it->second<<endl;
        it++;
        // cout<<" "<<endl;
    }

    // In unordered map things are printed in random order
    // Similarly in map complexity is log n time and it is based on BST

    return 0;
}