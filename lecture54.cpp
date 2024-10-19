#include<iostream>
using namespace std;

class Stack{
    public:
        int *arr;
        int top;
        int size;

    Stack(int size){
        this ->size = size;
        arr = new int[size];

        top=-1;
    }

    void push(int element){
        if(size-top >1){
            top++;
            arr[top] = element;
        }
        else{
            cout<<"Stack Overflow"<<endl;
        }
    }

    void pop(){
        if(top>=0){
            top--;
        }
        else{
            cout<<"Stack Underflow"<<endl;
        }
    }

    int peek(){
        if(top>=0){
            return arr[top];
        }
        else{
            cout<<"Stack is empty"<<endl;
            return -1;
        }
    }

    bool isEmpty(){
        if(top==-1){
            return true;
        }
        else{
            return false;
        }
    }
};


int main(){

    Stack st(5);
    st.push(22);
    st.push(33);


    cout<<st.peek();
    return 0;
}