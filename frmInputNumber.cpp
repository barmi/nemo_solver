//
// Created by skshin on 2021/05/16.
//

#include <QPlainTextEdit>
#include <QGridLayout>

#include "frmInputNumber.h"

frmInputNumber::frmInputNumber(const QString &title, QWidget *parent, bool isRow, int num)
    : QDialog(parent)
{
    auto *layout = new QGridLayout;
    if (isRow) {
        int row = num;
        int col = (num + 1) / 2;
        QPlainTextEdit *edit[row * col];

        for (int y = 0; y < row; y++) {
            for (int x = 0; x < col; x++) {
                auto t_edit  = new QPlainTextEdit(this);
                t_edit->setTabChangesFocus(true);
                t_edit->setFixedSize(30, 20);
                layout->addWidget(t_edit, y, x);
                edit[y * col + x] = t_edit;
            }
        }
    }
    else {
        int col = num;
        int row = (num + 1) / 2;
        QPlainTextEdit *edit[col * row];

        for (int x = 0; x < col; x++) {
            for (int y = 0; y < row; y++) {
                auto t_edit  = new QPlainTextEdit(this);
                t_edit->setTabChangesFocus(true);
                t_edit->setFixedSize(30, 20);
                layout->addWidget(t_edit, y, x);
                edit[y * col + x] = t_edit;
            }
        }
    }
    setLayout(layout);
}
