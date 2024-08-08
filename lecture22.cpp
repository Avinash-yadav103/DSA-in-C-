#include<iostream>
#include<vector>
using namespace std;

char toLowerCase(char name){
    if(name>= 'a' && name <='z'){
        return name;
    }
    else{
        char temp = name - 'A' + 'a';
        return temp;
    }
}

int getLength(char name[]){
    int count = 0;
    for(int i = 0; ;i++){
        if(name[i]=='\0') {break;}
        count++;
        
    }
    return count;
}

void reverse(char name[], int n){
    int s = 0;
    int e = n-1;
    while(s<e){
        swap(name[s++],name[e--]);
    }
}

string reverseString(string s) {
    int n = s.length();
    int start = 0;
    int end = n - 1;
    
    while (start < end) {
        swap(s[start], s[end]);
        start++;
        end--;
    }
    
    return s;
}
 
bool palindrome(char name[], int n){
    int s = 0;
    int e = n-1;
    while(s<n){
        if(toLowerCase(name[s])==toLowerCase(name[e])){
            s++;e--;
        }
        else{
            return false;
        }
    }
    return true;
}           

//Question : Reverse words of string
string reversedStr(string s){
    string temp ="";
    for(int i =0; i<s.length();i++){
        if(s[i]==' '){  //Remember single quote here
            reverseString(s);
            // s.push_back();
            // temp.push_back(s[i]);
        }
    }
    return s;
}

vector<char> Hello(vector<char> ch){
    // int s = 0;

    // for(int i=0;i<ch.size()-1;i++){
        
    //     if(ch[i]=='\0'){
    //         int e = i;
    //         while(s<e){
    //             swap(s++,e--);
    //         }
    //     }
    //     int s = i;
    // }

    // return ch;

    
}


int main(){
    string th = "This is my name avinash";
    cout<<reversedStr(th);

    // char name[20];

    // cout << "Enter you name "<<endl;
    // cin >> name;
    // // name[2] = '\0'; 
    
    // cout << "Your name is ";
    // cout << name;

    // cout << "Length: "<< getLength(name) << endl; 
    // int len = getLength(name);
    // reverse(name , len);

    // cout<<"Your name is ";
    // cout<< name <<endl;

    // cout <<"Palidrome or not: "<< palindrome(name , len);



    return 0;
}