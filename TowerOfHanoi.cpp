#include<iostream>
using namespace std;

void TOH(int N, char source, char aux, char dest){
    int count=0;
    if(N>0){
        TOH(N-1,source,dest ,aux);
        cout<<"Move disc "<< N <<" from rod "<< source << " to rod " << dest <<endl;
        count++;
        TOH(N-1,aux,source,dest);
    }
    cout<<count;
}

int main(){
    int n;
    cout<<"Enter the number of disks: ";
    cin>>n;

    TOH(3,'A','B','C');
}