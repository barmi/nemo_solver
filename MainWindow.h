//
// Created by skshin on 2021/05/14.
//

#ifndef NEMO2_MAINWINDOW_H
#define NEMO2_MAINWINDOW_H

#include <QWidget>

class MainWindow : public QWidget
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

    void inputVerticalNumbers();

private:
    void paintEvent(QPaintEvent *event) override;
//    Ui::MainWindow *ui;
};

#endif //NEMO2_MAINWINDOW_H
