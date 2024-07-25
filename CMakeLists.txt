cmake_minimum_required(VERSION 3.21)
project(nemo_solver)

set(CMAKE_PREFIX_PATH "/opt/homebrew/opt/qt5/lib/cmake")
#set(CMAKE_INCLUDE_CURRENT_DIR ON)

set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Qt5 COMPONENTS
        Core
        Gui
        Widgets
        REQUIRED)

add_executable(nemo_solver
        main.cpp
        MainWindow.cpp
        MainWindow.h
        frmInputNumber.cpp
        frmInputNumber.h
        nemo_util.cpp
        nemo_util.h
        )

target_link_libraries(nemo_solver
        Qt5::Core
        Qt5::Gui
        Qt5::Widgets
        )


