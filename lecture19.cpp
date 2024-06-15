#include<iostream>
#include<array>
#include<vector>
#include<deque>
using namespace std;



void printingArray(int arr[], int n){
    for(int i=0;i<n;i++){
        cout<<arr[i]<<" ";
    }
}

int arr(){
    int basic[] ={1,2,3};

    array<int,4> a = {1,2,3,4};
    int size =a.size();

    for(int i=0;i<size;i++){
        cout<<a[i]<<" ";
    }

    cout<<"Element at 2nd Index-"<<a.at(2)<<endl;
    cout<<"Empty or not-"<<a.empty()<<endl;
    cout<<"First Element-"<<a.front()<<endl;
    cout<<"Last Element-"<<a.back()<<endl;
    //We can access this with time complexity O(1)

}

int vec(){
    //Initializing all elements with 1
    vector<int> v1(5,1);

    //checking size of vector
    cout<<"Size of vector-"<<v1.size()<<endl;
    // capacity of vector
    cout<<"Capacity of vector-"<<v1.capacity()<<endl;
    //Difference in size and capacity
    // cout<<"Difference in size and capacity-"<<v.max_size()<<endl;
    // Difference is vector capacity is the maximum number of
    // elements that a vector can hold at a time whereas size
    // is the number of elements currently present in the vector.
 
    vector<int> v = {1,2,3,4,5};
    //To add element at the end
    v.push_back(6);
    //To remove element from the end
    v.pop_back();
    //To insert element at the beginning
    v.insert(v.begin()+2,8);
    //To remove element from the beginning
    v.erase(v.begin()+2);
    //To remove all elements
    v.clear();
    
    v.size();
    //To check if vector is empty or not
    v.capacity();
    //To increase the capacity of vector
    v.resize(10);
    //To decrease the capacity of vector
    v.reserve(100);
    v.shrink_to_fit();
    v.empty();
    v.front();
    v.back();
    v.at(2);
    v[2];
    v.begin();
    v.end();
    v.rbegin();
    v.rend();
    v.insert(v.begin()+2,3,7);
    v.erase(v.begin()+2,v.begin()+5);
    v.assign(5,10);
    v.swap(v);
    v.emplace(v.begin()+2,8);

}

int deq(){
    deque<int> dq = {1,2,3,4,5};
    //To add element at the end
    dq.push_back(6);
    //To add element at the front
    dq.push_front(0);
    //To remove element from the end
    dq.pop_back();
    //To remove element from the front
    dq.pop_front();
    //To check the size of deque
    dq.size();
    //To check if deque is empty or not
    dq.empty();
    //accessing the first element
    dq.front();
    //accessing the last element
    dq.back();
    //accessing the element at 2nd index
    dq.at(2);
    //accessing the element at 2nd index
    dq[2];
    //To get the iterator to the beginning
    dq.begin();
    //To get the iterator to the end
    dq.end();
    //To get the reverse iterator to the beginning
    dq.rbegin();
    //To get the reverse iterator to the end
    dq.rend();
    //To insert 3 elements with value 7 at 2nd index
    dq.insert(dq.begin()+2,3,7);
    //To remove elements from 2nd index to 5th index.
    //It needs two iterators
    dq.erase(dq.begin()+2,dq.begin()+5);
    //To assign 5 elements with value 10
    dq.assign(5,10);
    //To swap two deques
    dq.swap(dq);
    //To insert element at 2nd index
    dq.emplace(dq.begin()+2,8);

}

int main(){
    deque<int> dq = {1,2,3,4,5};
    // cout<<dq.front();
    //You cannot directly use std::cout with dq.begin() because dq.begin() returns an iterator, not the value itself.
    dq.begin();
    return 0;
}   