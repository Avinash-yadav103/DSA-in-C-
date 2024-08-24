// #include<iostream>
// #include<vector>
// using namespace std;

// vector<int> plusOne(vector<int>& digits){
//     // for(int i =0;i<digits.size();i++){
//     //     // cin>>digits[i];
//     //     if(i==digits.size()){
//     //         digits[i] = digits[i] + 1;
//     //     }
//     // }
//     int count = 0;
//     if(digits[digits.size()-1]==9){
//             // digits[i]=0;
//             vector<int> newarr(digits.size()+1);
//             newarr.push_back(1);
//             for(int i=0;i<digits.size();i++){
//                 digits.push_back(0);
//             }
            
//         return newarr;
//     } 
//     for(int i =digits.size();i>0;i--){


//         if(digits[i]<=9){
//             ++digits[i];
//             // return digits;
//             break;
//         }
        
//        return digits;
//     }
    
  
//     //Printing value
//     for(int i =0;i<digits.size();i++){
//         cout<<digits[i]<<" ";
//     }
// }

// int main(){
//     vector<int> hello = {1,9};

//     plusOne(hello);
//     return 0;
// }