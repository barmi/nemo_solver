//
// Created by skshin on 2021/05/16.
//

#ifndef NEMO_SOLVER_FRMINPUTNUMBER_H
#define NEMO_SOLVER_FRMINPUTNUMBER_H

#include <QDialog>

class frmInputNumber : public QDialog
{
    Q_OBJECT

private:
    int row, col;
    bool is_row;
    int cur_x, cur_y;
    void setCellColor(const QColor &color);

public:
    frmInputNumber(const QString &title, QWidget *parent, bool isRow, int num);

public slots:
    void verify();

protected:
    void keyPressEvent(QKeyEvent *keyevent);

};


#endif //NEMO_SOLVER_FRMINPUTNUMBER_H
