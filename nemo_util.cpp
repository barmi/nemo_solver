//
// Created by skshin on 2021/05/17.
//

#include <string>
#include <vector>
#include <numeric>
#include "nemo_util.h"

using namespace std;

/*
 * base에 부합되는 str인지 비교한다.
 */
static bool compare_base_str(string& base_str, string& str)
{
    for (int j = 0; j < str.size(); j++) {
        if (!base_str.empty() && base_str[j] != ' ' && base_str[j] != str[j])
            return false;
    }
    return true;
}

void find_all_seq(int size, seq_t seq, const string& pre, /*seq_str_t &seq_str,*/ string& base_str, string& comp_str)
{
    int first = seq[0];
    seq_t seq2(seq.begin() + 1, seq.end());
    if (seq2.empty()) {
        for (int i = 0; i <= size - first; i++) {
            //cout << pre + string(i, 'x') + string(first, 'o') + string(size - first - i, 'x') << "\n";
            string str = pre + string(i, 'x') + string(first, 'o') + string(size - first - i, 'x');
            //seq_str.push_back(str);
            if (!compare_base_str(base_str, str))
                continue;
            if (comp_str.empty())
                comp_str = str;
            for (int j = 0; j < str.size(); j++) {
                if (comp_str[j] != ' ' && comp_str[j] != str[j])
                    comp_str[j] = ' ';
            }
           // cout << comp_str << "\n";
        }
        return;
    }
    int rest_sum = accumulate(seq2.begin(), seq2.end(), 0);
    int rest_count = size - (rest_sum + seq2.size() - 1) - (first + 1);

    for (int i = 0; i <= rest_count; i++) {
        for (int j = 0; j <= i; j++) {
            find_all_seq(size - first - i - 1,
                         seq2,
                         pre + string(j, 'x') + string(first, 'o') + string(i-j, 'x') + "x",
                         //seq_str,
                         base_str,
                         comp_str);
        }
    }
}
