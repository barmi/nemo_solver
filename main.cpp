#include <iostream>
#include <vector>
#include <string>
#include <numeric>

#include "MainWindow.h"
#include <QApplication>

using namespace std;

int main(int argc, char *argv[])
{
    /*
    seq_t seq = { 0 };
    seq_str_t seq_str;
    string base_str;// = " O           ";
    string comp_str;

    find_all_seq(10, seq, "", seq_str, base_str, comp_str);
//    for (auto str: seq_str)
//        cout << str << "\n";
    cout << "\n" << base_str << "\n";
    cout << "\n" << comp_str << "\n";
*/

    QApplication a(argc, argv);
    MainWindow w;
    w.show();
    return a.exec();
}
