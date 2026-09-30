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

# The dqrobotics headers include both <Eigen/Dense> and <eigen3/Eigen/Dense>.
# The Eigen3 package provides <prefix>/include/eigen3, which resolves the first;
# the second needs <prefix>/include, which is on the default search path on
# Linux (/usr/include) and Windows (the vcpkg include root) but not on macOS
# (Homebrew's /opt/homebrew/include). Rather than adding all of that prefix
# (which could shadow, e.g., the pybind11 submodule with a Homebrew pybind11),
# expose only Eigen: a directory in the build tree holding an "eigen3" link to
# Eigen's include directory. include_directories applies to sas_cpp as well,
# since it is added below.
find_package(Eigen3 REQUIRED)
if(NOT WIN32)
    get_target_property(_eigen3_include_dirs Eigen3::Eigen INTERFACE_INCLUDE_DIRECTORIES)
    list(GET _eigen3_include_dirs 0 _eigen3_include_dir)
    set(_eigen3_shim "${CMAKE_BINARY_DIR}/eigen3_include_shim")
    file(MAKE_DIRECTORY "${_eigen3_shim}")
    if(NOT EXISTS "${_eigen3_shim}/eigen3")
        file(CREATE_LINK "${_eigen3_include_dir}" "${_eigen3_shim}/eigen3" SYMBOLIC)
    endif()
    include_directories(SYSTEM "${_eigen3_shim}")
endif()

add_subdirectory(submodules/sas_cpp)

set(PYBIND11_FINDPYTHON ON)
add_subdirectory(submodules/pybind11)

pybind11_add_module(_core MODULE
    src/sas_core_py.cpp
    src/sas_robot_driver_py.cpp
    src/sas_modeling_py.cpp
)

target_link_libraries(_core PRIVATE marinholab::sas::core)
