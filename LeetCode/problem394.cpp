class Solution {
public:
    string decodeString(string s) {
        // We can use Recursion
        // int i = 0;
        // return decode(s, i);

        // Using Stack (Easier Approach)
        stack<char> st;
        for(int i =0;i<s.size();i++){
            if(s[i] != ']'){
                st.push(s[i]);
            }
            else{
                string curr_str ="";
                while(st.top() != '['){
                    curr_str = st.top() + curr_str ;
                    st.pop();
                }
                st.pop(); //this is for [

                string number = "";

                while( !st.empty() && isdigit(st.top())){
                    number = st.top() + number;
                    st.pop(); 
                }
                int k = stoi(number);
                while(k--){
                    for(int i =0;i<curr_str.size(); i++){
                        st.push(curr_str[i]);
                    }
                }
            }
        }
        s = "";
        while(!st.empty()){
            s = st.top() + s;
            st.pop();
        }
        return s;
    }

    // string decode(string &s , int &i){
    //     string result = "";
    //     int num = 0;
    //     for(char i: s){
    //         char c = i;
    //         if(isdigit(c)){
    //             num = num*10 + (c -'0');
    //         }

    //     }
    // }
};