//
// Created by skshin on 2021/05/14.
//

#include <QPushButton>
#include <QGridLayout>
#include <QLabel>
#include <QPlainTextEdit>

#include "MainWindow.h"
#include "frmInputNumber.h"

MainWindow::MainWindow(QWidget *parent)
        : QWidget(parent)
{
    setWindowTitle("NemoNemo Solver");

    auto *label1 = new QLabel("가로크기:", this);
    m_edit_col = new QPlainTextEdit(this);
    m_edit_col->setTabChangesFocus(true);
    m_edit_col->setFixedSize(60, 30);
    m_edit_col->setPlainText("20");
    auto *label2 = new QLabel("세로크기:", this);
    m_edit_row = new QPlainTextEdit(this);
    m_edit_row->setTabChangesFocus(true);
    m_edit_row->setFixedSize(60, 30);
    m_edit_row->setPlainText("20");

    auto *button1 = new QPushButton("가로입력", this);
    button1->setGeometry(0, 0, 150, 40);
    connect(button1, &QPushButton::clicked, this, &MainWindow::inputVerticalNumbers);
    button1->show();

    auto *button2 = new QPushButton("세로입력",  this);
    button2->setGeometry(160, 0, 150, 40);
    connect(button2, &QPushButton::clicked, this, &MainWindow::inputHorizontalNumbers);
    button2->show();

    auto *layout = new QGridLayout;
    layout->addWidget(label1, 0, 0);
    layout->addWidget(m_edit_col, 0, 1);
    layout->addWidget(label2, 0, 2);
    layout->addWidget(m_edit_row, 0, 3);
    layout->addWidget(button1, 1, 0, 1, 2);
    layout->addWidget(button2, 1, 2, 1, 2);

    setLayout(layout);
}

MainWindow::~MainWindow()
= default;

void MainWindow::paintEvent(QPaintEvent *event)
{
    //
}

void MainWindow::inputVerticalNumbers()
{
//    QString text = "col=" + m_edit_col.toPlainText() + ", row=" + m_edit_row.toPlainText();
//    QMessageBox::information(this, "info", text);
    auto frm = new frmInputNumber("", this, true, m_edit_row->toPlainText().toInt());
    frm->exec();
}

void MainWindow::inputHorizontalNumbers()
{
    auto frm = new frmInputNumber("", this, false, m_edit_col->toPlainText().toInt());
    frm->exec();
}
