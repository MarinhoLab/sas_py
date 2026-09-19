# https://pybind11.readthedocs.io/en/stable/compiling.html
cmake_minimum_required(VERSION 3.16)

if(WIN32)
    set(CMAKE_TOOLCHAIN_FILE C:/vcpkg/scripts/buildsystems/vcpkg.cmake)
endif()

project(marinholab_sas_py LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# The pybind11 module is self-contained: build marinholab_sas_core as a static
# library and link it into _core, so the resulting extension module has no
# dependency on a separately installed marinholab_sas_core shared library.
# (Matches the working-needlemanipulation approach, where dqrobotics is built
# in-tree as static.)
set(BUILD_SHARED_LIBS OFF CACHE BOOL "" FORCE)
set(MARINHO_LAB_SAS_CORE_BUILD_EXAMPLES OFF CACHE BOOL "" FORCE)

add_subdirectory(submodules/sas_cpp)

set(PYBIND11_FINDPYTHON ON)
add_subdirectory(submodules/pybind11)

pybind11_add_module(_core MODULE
    src/sas_core_py.cpp
    src/sas_robot_driver_py.cpp
)

target_link_libraries(_core PRIVATE marinholab::sas::core)
