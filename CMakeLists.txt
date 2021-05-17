cmake_minimum_required(VERSION 3.19)
project(nemo_solver)

set(CMAKE_PREFIX_PATH "/usr/local/Cellar/qt/5.15.2/lib/cmake")
set(CMAKE_INCLUDE_CURRENT_DIR ON)

set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Qt5Widgets REQUIRED)
find_package(QT NAMES Qt6 Qt5 COMPONENTS Widgets REQUIRED)
find_package(Qt${QT_VERSION_MAJOR} COMPONENTS Widgets REQUIRED)

add_executable(nemo_solver
        main.cpp
        MainWindow.cpp
        MainWindow.h
        frmInputNumber.cpp
        frmInputNumber.h
        nemo_util.cpp
        nemo_util.h
        )

target_link_libraries(nemo_solver PRIVATE Qt5::Widgets)

