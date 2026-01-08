// #include <bits/stdc++.h>
#include<iostream>
#include<vector>
#include<algorithm>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    if (!(cin >> N)) return 0;
    vector<string> words;
    words.reserve(N);
    for (int i = 0; i < N; ++i) {
        string s;
        if (!(cin >> s)) break;
        words.push_back(s);
    }

    auto transform = [](const string& s) {
        array<int, 26> freq{};
        for (char c : s) freq[c - 'a']++;
        vector<pair<char,int>> items;
        items.reserve(26);
        for (int i = 0; i < 26; ++i) {
            if (freq[i] > 0) items.emplace_back(char('a' + i), freq[i]);
        }
        sort(items.begin(), items.end(), [](const auto& a, const auto& b) {
            if (a.second != b.second) return a.second < b.second; // increasing frequency
            return a.first > b.first; // later lexicographical first
        });
        string out;
        out.reserve(s.size());
        for (auto [ch, f] : items) out.append(f, ch);
        return out;
    };

    for (size_t i = 0; i < words.size(); ++i) {
        if (i) cout << ' ';
        cout << transform(words[i]);
    }
    return 0;
}