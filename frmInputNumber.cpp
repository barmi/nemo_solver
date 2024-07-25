//
// Created by skshin on 2021/05/16.
//

#include <QPlainTextEdit>
#include <QGridLayout>
#include <QDialogButtonBox>

#include "frmInputNumber.h"
#include "MainWindow.h"

frmInputNumber::frmInputNumber(const QString &title, QWidget *parent, bool isRow, int num)
    : QDialog(parent)
{
    is_row = isRow;
    auto *layout = new QGridLayout;
    MainWindow *w = (MainWindow *)parent;

    cur_x = cur_y = 0;
    if (isRow) {
        row = num;
        col = (num + 1) / 2;
        QPlainTextEdit *edit[row * col];

        for (int y = 0; y < row; y++) {
            for (int x = 0; x < col; x++) {
                auto t_edit = new QPlainTextEdit(this);
                t_edit->setTabChangesFocus(true);
                t_edit->setFixedSize(40, 25);
                t_edit->setObjectName(QString("edit_") + QString::number(x) + "_" + QString::number(y));
                if (!w->label_row.empty() && w->label_row[y].size() > x) {
                    t_edit->setPlainText(QString::number(w->label_row[y][x]));
                }
                t_edit->setVerticalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
                t_edit->setEnabled(false);
                QPalette p = t_edit->palette();
                p.setColor(QPalette::Base, (x == cur_x && y == cur_y) ? Qt::red : Qt::lightGray);
                t_edit->setPalette(p);
                layout->addWidget(t_edit, y, x);
                edit[y * col + x] = t_edit;
            }
        }
    }
    else {
        col = num;
        row = (num + 1) / 2;
        QPlainTextEdit *edit[col * row];

        for (int x = 0; x < col; x++) {
            for (int y = 0; y < row; y++) {
                auto t_edit = new QPlainTextEdit(this);
                t_edit->setTabChangesFocus(true);
                t_edit->setFixedSize(40, 20);
                t_edit->setObjectName(QString("edit_") + QString::number(x) + "_" + QString::number(y));
                if (!w->label_col.empty() && w->label_col[x].size() > y) {
                    t_edit->setPlainText(QString::number(w->label_col[x][y]));
                }
                t_edit->setVerticalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
                t_edit->setEnabled(false);
                layout->addWidget(t_edit, y, x);
                edit[y * col + x] = t_edit;
            }
        }
    }

    auto buttonBox = new QDialogButtonBox(QDialogButtonBox::Ok | QDialogButtonBox::Cancel);
    connect(buttonBox, &QDialogButtonBox::accepted, this, &frmInputNumber::verify);
    connect(buttonBox, &QDialogButtonBox::rejected, this, &frmInputNumber::reject);
    layout->addWidget(buttonBox, row, 0, 1, col);

    setLayout(layout);
}

void frmInputNumber::verify()
{
    MainWindow *w = (MainWindow *)parent();
    if (is_row) {
        w->label_row.clear();
        for (int y = 0; y < row; y++) {
            vector<uint8_t> l;
            for (int x = 0; x < col; x++) {
                QPlainTextEdit* edit = this->findChild<QPlainTextEdit*>(QString("edit_") + QString::number(x) + "_" + QString::number(y));
                if (!edit->toPlainText().isEmpty()) {
                    l.push_back(edit->toPlainText().toInt());
                }
            }
            w->label_row.push_back(l);
        }
    }
    else {
        w->label_col.clear();
        for (int x = 0; x < col; x++) {
            vector<uint8_t> l;
            for (int y = 0; y < row; y++) {
                QPlainTextEdit* edit = this->findChild<QPlainTextEdit*>(QString("edit_") + QString::number(x) + "_" + QString::number(y));
                if (!edit->toPlainText().isEmpty()) {
                    l.push_back(edit->toPlainText().toInt());
                }
            }
            w->label_col.push_back(l);
        }
    }
    accept();
}

void frmInputNumber::keyPressEvent(QKeyEvent *keyevent) {
    if (keyevent->key() == Qt::Key_D) {
        setCellColor(Qt::lightGray);
        cur_x++;
        setCellColor(Qt::red);
        return;
    }
    else if (keyevent->key() == Qt::Key_S) {
        setCellColor(Qt::lightGray);
        cur_y++;
        setCellColor(Qt::red);
        return;
    }
    else if (keyevent->key() == Qt::Key_A) {
        setCellColor(Qt::lightGray);
        cur_x--;
        setCellColor(Qt::red);
        return;
    }
    else if (keyevent->key() == Qt::Key_W) {
        setCellColor(Qt::lightGray);
        cur_y--;
        setCellColor(Qt::red);
        return;
    }
    else if (keyevent->key() >= Qt::Key_0 && keyevent->key() <= Qt::Key_9) {
        QPlainTextEdit* edit = this->findChild<QPlainTextEdit*>(QString("edit_") + QString::number(cur_x) + "_" + QString::number(cur_y));
        edit->setPlainText(QString(keyevent->key()));
        setCellColor(Qt::lightGray);
        if (is_row)
            cur_x++;
        else
            cur_y++;
        setCellColor(Qt::red);
        return;
    }
    else if (keyevent->key() == Qt::Key_Q) {
        setCellColor(Qt::lightGray);
        if (is_row) {
            cur_x = 0;
            cur_y++;
        }
        else {
            cur_x++;
            cur_y = 0;
        }
        setCellColor(Qt::red);
        return;
    }

    QDialog::keyPressEvent(keyevent);
}

void frmInputNumber::setCellColor(const QColor &color)
{
    QPlainTextEdit* edit = this->findChild<QPlainTextEdit*>(QString("edit_") + QString::number(cur_x) + "_" + QString::number(cur_y));
    QPalette p = edit->palette();
    p.setColor(QPalette::Base, color);
    edit->setPalette(p);
}

