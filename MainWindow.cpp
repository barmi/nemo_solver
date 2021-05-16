//
// Created by skshin on 2021/05/14.
//

#include <QPushButton>
#include "MainWindow.h"

MainWindow::MainWindow(QWidget *parent)
        : QWidget(parent)
{
    setWindowTitle("NemoNemo");
    QPushButton *button = new QPushButton("가로입력", this);
    button->setGeometry(0, 0, 150, 40);
    connect(button, &QPushButton::clicked, this, &MainWindow::inputVerticalNumbers);
    button->show();
    button = new QPushButton("세로입력",  this);
    button->setGeometry(160, 0, 150, 40);
    button->show();

}

MainWindow::~MainWindow()
{

}

void MainWindow::paintEvent(QPaintEvent *event)
{
    //
}

void MainWindow::inputVerticalNumbers()
{

}