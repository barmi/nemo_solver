//
// Created by skshin on 2021/05/17.
//

#ifndef NEMO_SOLVER_NEMO_UTIL_H
#define NEMO_SOLVER_NEMO_UTIL_H

using namespace std;

typedef vector<u_int8_t> seq_t;
typedef vector<string>   seq_str_t;

void find_all_seq(int size, seq_t seq, const string& pre, /*seq_str_t &seq_str,*/ string& base_str, string& comp_str);

#endif //NEMO_SOLVER_NEMO_UTIL_H
