#include<iostream>
using namespace std;

void update(int **p){
    p=p+1;

    *p = *p+1;

    **p = **p+1;
}

int main(){

    int i =5;
    int* p = &i;
    int** p2 =&p;

    cout<<endl<<endl<<"Ok"<<endl;
    cout<<"printing p: "<<p<<endl;
    cout<<"address of p: "<<&p<<endl;
    cout<<*p2<<endl;

    cout<<i<<endl;
    cout<<*p<<endl;
    cout<<**p2<<endl;

    cout<<&i<<endl;
    cout<<p<<endl;
    cout<<*p2<<endl;

    cout<<&p<<endl;
    cout<<p2<<endl;


    return 0;
}