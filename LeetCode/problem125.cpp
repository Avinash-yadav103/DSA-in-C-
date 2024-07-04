#include<iostream>
using namespace std;


// private:
//     char valid(char ch){
//         if((ch>='a' &&  ch<='z') || (ch>='A' && ch<='Z') || (ch>='0' && ch<='9')){
//             return 1;
//         }   
//         return 0;
//     }

//     char toLowerCase(char ch){
//         if((ch>= 'a' && ch <='z') || (ch>='0' && ch<='9')){
//             return ch;
//         }
//         else{
//             char temp = ch - 'A' + 'a';
//             return temp;
//         }
//     }

//     bool palindrome(string name){
//     int s = 0;
//     int e = name.length()-1;
//     while(s<e){
//         if(name[s]==name[e]){
//             s++;e--;
//         }
//         else{
//             return false;
//         }
//     }
//     return true;
// }           

// public:
//     bool isPalindrome(string s) {
//         string temp = "";
//         for(int i = 0; i<s.length();i++){
//             if(valid(s[i])){
//                 temp.push_back(s[i]);
//             }
//         }


//         //lowercase check
//         for(int i=0;i<temp.length();i++){
//             temp[i] = toLowerCase(temp[i]);
//         }

//         return palindrome(temp);
//     }




// int main(){








//     return 0;
// }