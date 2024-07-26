//
// Created by skshin on 2021/05/14.
//

#include <QPushButton>
#include <QGridLayout>
#include <QLabel>
#include <QPlainTextEdit>
#include <QFileDialog>

#include <iostream>
#include <QPainter>

#include "MainWindow.h"
#include "frmInputNumber.h"
#include "nemo_util.h"

MainWindow::MainWindow(QWidget *parent)
        : QWidget(parent), board(nullptr)
{
    setWindowTitle("NemoNemo Solver");

    auto *label1 = new QLabel("가로크기:", this);
    m_edit_col = new QPlainTextEdit(this);
    m_edit_col->setTabChangesFocus(true);
    m_edit_col->setFixedSize(60, 30);
    //m_edit_col->setPlainText("20");
    auto *label2 = new QLabel("세로크기:", this);
    m_edit_row = new QPlainTextEdit(this);
    m_edit_row->setTabChangesFocus(true);
    m_edit_row->setFixedSize(60, 30);
    //m_edit_row->setPlainText("20");

    auto *button1 = new QPushButton("가로입력", this);
    button1->setFixedSize(150, 40);
    connect(button1, &QPushButton::clicked, this, &MainWindow::inputVerticalNumbers);
    button1->show();

    auto *button2 = new QPushButton("세로입력",  this);
    button2->setFixedSize(150, 40);
    connect(button2, &QPushButton::clicked, this, &MainWindow::inputHorizontalNumbers);
    button2->show();

    auto *layout = new QGridLayout;
    layout->addWidget(label1, 0, 0);
    layout->addWidget(m_edit_col, 0, 1);
    layout->addWidget(label2, 0, 2);
    layout->addWidget(m_edit_row, 0, 3);
    layout->addWidget(button1, 1, 0, 1, 2);
    layout->addWidget(button2, 1, 2, 1, 2);

    auto *button = new QPushButton("Load", this);
    button->setFixedSize(150, 40);
    connect(button, &QPushButton::clicked, this, &MainWindow::FileLoad);
    layout->addWidget(button, 2, 0, 1, 2);

    button = new QPushButton("Save", this);
    button->setFixedSize(150, 40);
    connect(button, &QPushButton::clicked, this, &MainWindow::FileSave);
    layout->addWidget(button, 2, 2, 1, 2);

    button = new QPushButton("풀기", this);
    button->setFixedSize(150, 40);
    connect(button, &QPushButton::clicked, this, &MainWindow::Process);
    layout->addWidget(button, 3, 0, 1, 2);

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
    auto frm = new frmInputNumber("", this, true, m_edit_row->toPlainText().toInt());
    frm->exec();
}

void MainWindow::inputHorizontalNumbers()
{
    auto frm = new frmInputNumber("", this, false, m_edit_col->toPlainText().toInt());
    frm->exec();
}

void MainWindow::FileLoad()
{
    QString fname = QFileDialog::getOpenFileName(this,
                                                 "불러올 파일 선택",
                                                 QDir::currentPath() + "/data",
                                                 "Files (*.*)");
    load_file_name = fname.toStdString();
    FILE *fp;

    int sizex, sizey;
    if ((fp = fopen(fname.toStdString().c_str(), "rt"))) {
        label_col.clear();
        label_row.clear();

        int sum = 0;
        fscanf(fp, "%d %d", &sizex, &sizey);
        for (int i = 0; i < sizex; i++) {
            int num;
            vector<uint8_t> l;
            fscanf(fp, "%d", &num);
            for (int j = 0; j < num; j++) {
                int label;
                fscanf(fp, "%d", &label);
                l.push_back(label);
                sum += label;
            }
            label_col.push_back(l);
        }
        cout << "세로합 : " << sum << endl;

        sum = 0;
        for (int i = 0; i < sizey; i++) {
            int num;
            vector<uint8_t> l;
            fscanf(fp, "%d", &num);
            for (int j = 0; j < num; j++) {
                int label;
                fscanf(fp, "%d", &label);
                sum += label;
                l.push_back(label);
            }
            label_row.push_back(l);
        }
        cout << "가로합 : " << sum << endl;

        m_edit_col->setPlainText(QString::number(sizex));
        m_edit_row->setPlainText(QString::number(sizey));

        fclose(fp);
    }
}

void MainWindow::FileSave()
{
    QString fname = QFileDialog::getSaveFileName(this,
                                                 "저장할 파일 선택",
                                                 QDir::currentPath(),
                                                 "Files (*.*)");
    FILE *fp;

    if ((fp = fopen(fname.toStdString().c_str(), "wt"))) {
        auto sizex = label_col.size();
        auto sizey = label_row.size();

        fprintf(fp, "%lu %lu\n", sizex, sizey);
        for (const auto& i : label_col) {
            fprintf(fp, "%lu ", i.size());
            for (auto j : i) {
                fprintf(fp, "%d ", j);
            }
            fprintf(fp, "\n");
        }
        fprintf(fp, "\n");
        for (const auto& i : label_row) {
            fprintf(fp, "%lu ", i.size());
            for (auto j : i) {
                fprintf(fp, "%d ", j);
            }
            fprintf(fp, "\n");
        }

        fclose(fp);
    }
}

void MainWindow::Process()
{
    delete [] board;

    int w = m_edit_col->toPlainText().toInt();
    int h = m_edit_row->toPlainText().toInt();
    board = new char[ w * h ];
    memset(board, ' ', w * h);
    bool is_continue;
    int try_count = 0;
    do {
        is_continue = false;
        for (int y = 0; y < h; y++) {
            string line = string(w, ' ');
            int blank_count = 0;
            for (int x = 0; x < w; x++) {
                line[x] = board[y * w + x];
                if (line[x] == ' ') {
                    ++blank_count;
                }
            }
            if (blank_count == 0) {
                cout << line << "\n";
            }
            else {
                string guess;
                seq_t seq;
                seq.assign(label_row[y].begin(), label_row[y].end());
                // 모두 비어 있고, 확정할 수 없는 라인이면 찾지 않는다. (건너 뛴다)
                if (line == string(w, ' ') && (w - (accumulate(seq.begin(), seq.end(), 0) + seq.size() - 1)) >=
                                              *max_element(seq.begin(), seq.end()))
                    guess = string(w, ' ');
                else
                    find_all_seq(w, seq, "", line, guess);

                for (int x = 0; x < w; x++) {
                    if (board[y * w + x] != guess[x]) {
                        is_continue = true;
                        board[y * w + x] = guess[x];
                    }
                }
                cout << guess << "\n";
            }
        }
        cout << "----------------------\n";
        for (int x = 0; x < w; x++) {
            string line = string(h, ' ');
            int blank_count = 0;
            for (int y = 0; y < h; y++) {
                line[y] = board[y * w + x];
                if (line[y] == ' ') {
                    ++blank_count;
                }
            }
            if (blank_count > 0) {
                string guess;
                seq_t seq;
                seq.assign(label_col[x].begin(), label_col[x].end());
                // 모두 비어 있고, 확정할 수 없는 라인이면 찾지 않는다. (건너 뛴다)
                if (line == string(h, ' ') && (h - (accumulate(seq.begin(), seq.end(), 0) + seq.size() - 1)) >=
                                              *max_element(seq.begin(), seq.end()))
                    guess = string(h, ' ');
                else
                    find_all_seq(h, seq, "", line, guess);

                for (int y = 0; y < h; y++) {
                    if (board[y * w + x] != guess[y]) {
                        is_continue = true;
                        board[y * w + x] = guess[y];
                    }
                }
            }
        }
        for (int y = 0; y < h; y++) {
            string line = string(w, ' ');
            for (int x = 0; x < w; x++)
                line[x] = board[y * w + x];
            cout << line << "\n";
        }

        cout << try_count++ << " ------------------------\n";
    } while (is_continue);

    // 결과를 txt파일로 저장한다.
    string file_name = load_file_name + "_out.txt";
    FILE *fp;
    if ((fp = fopen(file_name.c_str(), "wt"))) {
        for (int y = 0; y < h; y++) {
            for (int x = 0; x < w; x++)
                fprintf(fp, "%c", (board[y * w + x] == 'x') ? '.' : board[y * w + x]);
            fprintf(fp, "\n");
        }
        fclose(fp);
    }

    for (int y = 0; y < h; y++) {
        for (int x = 0; x < w; x++)
            cout << (char)((board[y * w + x] == 'x') ? '.' : board[y * w + x]) ;
        cout << "\n";
    }

    // 연속된 숫자 찾기
    int * right_count = new int[w * h];
    int * down_count = new int[w * h];
    for (int y = 0; y < h; y++) {
        int count = 0;
        for (int x = 0; x < w; x++) {
            if (x == 0) {
                right_count[y * w + x] = 1;
            } else {
                if (board[y * w + x] == board[y * w + x - 1]) {
                    right_count[y * w + x] = right_count[y * w + x - 1] + 1;
                } else {
                    right_count[y * w + x] = 1;
                }
            }
            if (y == 0) {
                down_count[y * w + x] = 1;
            } else {
                if (board[y * w + x] == board[(y - 1) * w + x]) {
                    down_count[y * w + x] = down_count[(y - 1) * w + x] + 1;
                } else {
                    down_count[y * w + x] = 1;
                }
            }
        }
    }

    // 결과를 이미지로 저장
    int grid_size = 50;

    QImage img(grid_size * w, grid_size * h, QImage::Format_RGB32);
    img.fill(Qt::white);
    QPainter painter(&img);
    QPen pen_black(Qt::black, 1);
    QPen pen_gray(Qt::gray, 1);
    QPen pen_green(Qt::green, 1);

    painter.setPen(QPen(Qt::black, 1));
    // 그림에 숫자 표시
    QFont font = painter.font();
    font.setPixelSize(14);
    painter.setFont(font);


    QFontMetrics fm(font);
    for (int y = 0; y < h; y++) {
        for (int x = 0; x < w; x++) {
            if (board[y * w + x] == 'x') {
                painter.setBrush(QBrush(Qt::lightGray));
            }
            else {
                painter.setBrush(QBrush(Qt::black));
            }
            painter.setPen(QPen(Qt::white, 1));
            painter.drawRect(x * grid_size, y * grid_size, grid_size, grid_size);
            if ((x % 5) == 0 && x) {
                painter.setPen(QPen(Qt::magenta, 3));
                painter.drawLine(x * grid_size, y * grid_size, x * grid_size, (y + 1) * grid_size);
            }
            if ((y % 5) == 0 && y) {
                painter.setPen(QPen(Qt::magenta, 3));
                painter.drawLine(x * grid_size, y * grid_size, (x + 1) * grid_size, y * grid_size);
            }
            painter.setPen(QPen(Qt::green, 1));

            QString str = QString::number(right_count[y * w + x]);
            QRect rect = fm.boundingRect(str);
            painter.drawText(x * grid_size + int(grid_size * 0.75) - rect.width() / 2, y * grid_size + int(grid_size * 0.3) - rect.height()/2 + fm.ascent(), str);

            str = QString::number(down_count[y * w + x]);
            rect = fm.boundingRect(str);
            painter.setPen(QPen(Qt::red, 1));
            painter.drawText(x * grid_size + int(grid_size * 0.3) - rect.width() / 2, y * grid_size + int(grid_size * 0.75) - rect.height()/2 + fm.ascent(), str);
        }
    }
    painter.end();
    img.save(QString::fromStdString(load_file_name + "_out.png"));

    delete [] right_count;
    delete [] down_count;
}
