#include<iostream>
using namespace std;

int summation(int x , int y){
    int sum = x+y;
    return sum;
}

int size(int x){


    return 0;
}

int Max(int x , int y , int z){
    int p;
    if(x>y && x>z){
        p=x;
    }
    else if(y>z && y>x){
        p=y;
    }
    else{
        p=z;
    }

    return p;
}

int Min(int x , int y , int z){
    int p;
    if(x<y && x<z){
        p=x;
    }
    else if(y<z && y<x){
        p=y;
    }
    else{
        p=z;
    }

    return p;
}

int NaturalNum(int n){
    int i = 0;
    int num = n*(n+1)/2;

    return num;
}

int GCD(int x, int y){
    int p;
    int pro = 1;
    if(x>y){
        p=x;
    }
    else{
        p=y;
    }

    for(int i = 1;i<p;i++){
        if(x%i==0 && y%i ==0){
            pro = i;
        }
    }

    return pro;
}

void swapFunct(int &x, int &y){
    int temp = y;
    y = x;
    x = temp; 
    cout<<"Hello";
    cout<<summation(x,y);

}

int sizeL(int x){
    int p =sizeof(x);
    return p;

}

class point{
    int x , y ,z;

    public:
        point(int a){ x = y = z = a;}
        point(){x=y =z =0;}
        ~point(){
            cout<<"Deleting pt"<<x<<y<<z<<endl;

        }
};

int main (){
    cout<<"Hello World"<<endl;
    int x = 10;
    int y = 20;
    // swapFunct(x,y);
    cout<<sizeL(x)<<endl;
    cout<<GCD(x,y);
    point p2,p1(5);


    return 0;
}