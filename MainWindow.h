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
    string load_file_name;

    char *board;

    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow() override;

public slots:
    void inputVerticalNumbers();
    void inputHorizontalNumbers();
    void FileLoad();
    void FileSave();
    void Process();

private:
    void paintEvent(QPaintEvent *event) override;
//    Ui::MainWindow *ui;
    void LoadData();
};

#endif //NEMO2_MAINWINDOW_H
