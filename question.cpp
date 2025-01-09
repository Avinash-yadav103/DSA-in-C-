//Armstrong Number
#include<iostream>
#include<math.h>
using namespace std;

// void isArmstrong(int n){
//     // for number of digits
//     int count = 0;
//     int digit;
//     int sum = 0;
//     while(n!=0){
//         n = n/=10;
//         count++;
//     }

//     while(n!=0){
//         n = n/=10;
//         digit = n%10;
//         sum += pow(digit,count);

//     }

//     if(sum == n){
//         cout<<"Armstrong";
//     }
//     else{
//         cout<<"Not Armstrong";
//     }
// }

// int main(){
    
//     isArmstrong(153);
// }

class Node {
public:
    int data;
    string secret;
    Node* next;

    Node(int data,string secret) {
        this->data = data;
        this->secret = secret;
        this->next = nullptr;
    }
};

class LinkedList {
public:
    Node* head;

    LinkedList() {
        head = nullptr;
    }

    void insert(int data,string s) {
        Node* newNode = new Node(data,s);
        if (head == nullptr) {
            head = newNode;
        } else {
            Node* temp = head;
            while (temp->next != nullptr) {
                temp = temp->next;
            }
            temp->next = newNode;
        }
    }

    void display() {
        Node* temp = head;
        while (temp != nullptr) {
            cout << temp->data << " ";
            temp = temp->next;
        }
        cout << endl;
    }

    void findNth(int n) {
        Node* main_ptr = head;
        Node* refptr = head;

        int count = 0;
        if (head != nullptr) {
            while (count < n) {
                if (refptr == nullptr) {
                    cout << n << " is greater than the number of nodes in list" << endl;
                    return;
                }
                refptr = refptr->next;
                count++;
            }

            while (refptr != nullptr) {
                main_ptr = main_ptr->next;
                refptr = refptr->next;
            }

            cout << "The"<<n<< "th node from the end is"<< main_ptr->data << endl;
        }
    }
};

int main() {
    LinkedList list;
    list.insert(1,"hello");
    list.insert(2,"fellow");
    list.insert(3,"how");
    list.insert(4,"are");
    list.insert(5,"you");
    list.insert(6,"doing");
    list.display();


    list.findNth(4);
    return 0;
}