#include<iostream>
#include<array>
#include<vector>
#include<deque>
#include<list>
#include<stack>
#include<queue>
#include<set>
#include<map>
#include<algorithm>
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

int qu(){
    queue<int> q;
    //To add element at the end
    q.push(1);
    //To remove element from the front
    q.pop();
    //To check the size of queue
    q.size();
    //To check if queue is empty or not
    q.empty();
    //To access the front element
    q.front();
    //To access the back element
    q.back();
    //To swap two queues
    q.swap(q);
    //To insert element at the end
    q.emplace(2);
}

int li(){
    list<int> l = {1,2,3,4,5};
    //To add element at the end
    l.push_back(6);
    //To add element at the front
    l.push_front(0);
    //To remove element from the end
    l.pop_back();
    //To remove element from the front
    l.pop_front();
    //To check the size of list
    l.size();
    //To check if list is empty or not
    l.empty();
    //accessing the first element
    l.front();
    //accessing the last element
    l.back();
    

}

int stk(){
    stack<int, deque<int>> s;
    //To add element at the top
    s.push(1);
    //To remove element from the top
    s.pop();
    //To check the size of stack
    s.size();
    //To check if stack is empty or not
    s.empty();
    //To access the top element
    s.top();
    //To swap two stacks
    s.swap(s);
    //To insert element at the top
    s.emplace(2);
    
}

int pr_queue(){
    //max-heap creation
    priority_queue<int> maxi_pq;

    //min heap creation
    priority_queue<int,vector<int>,greater<int>> mini_pq;
    
    maxi_pq.push(1);
    maxi_pq.push(7);
    maxi_pq.push(5);
    maxi_pq.push(4);

    // Printing the numbers in the priority queue
    while (!maxi_pq.empty()) {
        cout << maxi_pq.top() << " ";
        maxi_pq.pop();
    }
    cout << endl;
    //Printing using for loop
    for(int i=0;i<mini_pq.size();i++){
        cout<<mini_pq.top()<<" ";
        mini_pq.pop();
    }    

    mini_pq.push(1);
    mini_pq.push(7);
    mini_pq.push(5);
    mini_pq.push(4);

    // Printing the numbers in the priority queue
    while (!mini_pq.empty()) {
        cout << mini_pq.top() << " ";
        mini_pq.pop();
    }
    cout << endl;

    //Printing using for loop
    for(int i=0;i<mini_pq.size();i++){
        cout<<mini_pq.top()<<" ";
        mini_pq.pop();
    }

}

int st(){
    set<int> s;
    //To add element
    s.insert(1);
    s.insert(1);
    s.insert(3);
    s.insert(3);
    s.insert(2);
    s.insert(2);

    //To remove element
    s.erase(2);
    //here 2 is index not the value

    //To check the size of set
    s.size();
    
    //To check number is present or not
    s.count(1);

    set<int>::iterator it = s.find(3);


}

int mp(){
    map<int,string> m;
    //To add element
    //here 1 is key and "one" is value
    m[1] = "one";
    m[2] = "two";
    //here 3 is key and "three" is value
    m.insert({3,"three"});

    //To remove element
    m.erase(2);
    //here 2 is index not the value

    //To check the size of map
    m.size();
    
    //To check number is present or not
    m.count(1);

    // map<int,int>::iterator it = m.find(3);
    //sorted in map 
    for(auto i:m){
        cout<<i.first<<" "<<i.second<<endl;
    }
}

int main(){
    
    vector<int> v;
    v.push_back(1);   
    v.push_back(3);
    v.push_back(6);
    v.push_back(7);

    cout<<"Finding 6 - "<<binary_search(v.begin(),v.end(),6)<<endl;

    cout<<"Lower Bound of 6 - "<<lower_bound(v.begin(),v.end(),6)-v.begin()<<endl;
    cout<<"Upper Bound of 6 - "<<upper_bound(v.begin(),v.end(),6)-v.begin()<<endl;

    int a = 5;
    int b = 6;
    cout<<"Max of 5 and 6 - "<<max(a,b)<<endl;
    cout<<"Min of 5 and 6 - "<<min(a,b)<<endl;

    // cout<<"Swap of 5 and 6 - "<<a<<" "<<b<<endl;
    swap(a,b);
    cout<<"Swap of 5 and 6 - "<<a<<" "<<b<<endl;

    string s = "Hello";
    reverse(s.begin(),s.end());
    cout<<"Reverse of Hello - "<<s<<endl;

    // Sort function
    int arr[] = {1,3,2,5,4};
    //This sort function is formed by intro sort
    //It is a hybrid sorting algorithm, derived from quicksort, heapsort, and insertion sort.
    sort(arr,arr+5);
    printingArray(arr,5);
    cout<<endl;
}   