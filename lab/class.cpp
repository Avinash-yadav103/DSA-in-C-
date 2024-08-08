#include<iostream>
using namespace std;

class point{
    int x , y ,z;

    public:
        point(int a){ x = y = z = a;}
        point(){x=y =z =0;}
        ~point(){
            cout<<"Deleting pt"<<x<<y<<z<<endl;

        }
};

