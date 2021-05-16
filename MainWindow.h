//
// Created by skshin on 2021/05/14.
//

#ifndef NEMO2_MAINWINDOW_H
#define NEMO2_MAINWINDOW_H

#include <QWidget>
#include <QPlainTextEdit>
#include <vector>

using namespace std;

class MainWindow : public QWidget
{
    Q_OBJECT

public:
    QPlainTextEdit *m_edit_col;
    QPlainTextEdit *m_edit_row;

    vector<vector<uint8_t>> label_row;
    vector<vector<uint8_t>> label_col;

    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow() override;

    void inputVerticalNumbers();
    void inputHorizontalNumbers();

private:
    void paintEvent(QPaintEvent *event) override;
//    Ui::MainWindow *ui;
};

#endif //NEMO2_MAINWINDOW_H
