# https://pybind11.readthedocs.io/en/stable/compiling.html
cmake_minimum_required(VERSION 3.16)

if(WIN32)
    set(CMAKE_TOOLCHAIN_FILE C:/vcpkg/scripts/buildsystems/vcpkg.cmake)
endif()

project(marinholab_sas_py LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# The pybind11 module is self-contained: dqrobotics (submodules/dqrobotics_cpp)
# and marinholab_sas_core (submodules/sas_cpp) are built from source as static
# libraries and linked into _core, so the extension module does not depend on
# any separately installed shared library. (This is the working-needlemanipulation
# approach.) The DQ and DQ_Kinematics objects that cross into Python are still
# the dqrobotics Python package's types: pybind11's type registry is shared
# between extension modules, so _core receives and returns the objects of the
# `dqrobotics` package. The two copies of dqrobotics must therefore have the
# same class layouts, which is why the submodule is pinned to the dqrobotics/cpp
# commit that the required `dqrobotics` Python release was built from.
set(BUILD_SHARED_LIBS OFF CACHE BOOL "" FORCE)
set(MARINHO_LAB_SAS_CORE_BUILD_EXAMPLES OFF CACHE BOOL "" FORCE)
set(MARINHO_LAB_SAS_CORE_INSTALL OFF CACHE BOOL "" FORCE)
# The static libraries end up in a shared object (_core), so they need PIC.
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
# Keep their symbols private to _core (pybind11 already builds _core itself
# with hidden visibility), so that they never interpose with the copy of
# dqrobotics inside the `dqrobotics` Python package's extension module.
set(CMAKE_CXX_VISIBILITY_PRESET hidden)
set(CMAKE_VISIBILITY_INLINES_HIDDEN ON)

find_package(Eigen3 REQUIRED)

# dqrobotics, as a static library. EXCLUDE_FROM_ALL: only what _core links is
# built. Its warning flags are PUBLIC compile options, which would propagate to
# everything that links it; they are for dqrobotics' own development, so drop
# them from its interface.
add_subdirectory(submodules/dqrobotics_cpp EXCLUDE_FROM_ALL)
set_property(TARGET dqrobotics PROPERTY INTERFACE_COMPILE_OPTIONS "")
# sas_cpp links dqrobotics::dqrobotics, and uses this target instead of looking
# for an installed dqrobotics when it is defined.
add_library(dqrobotics::dqrobotics ALIAS dqrobotics)

add_subdirectory(submodules/sas_cpp)

set(PYBIND11_FINDPYTHON ON)
add_subdirectory(submodules/pybind11)

pybind11_add_module(_core MODULE
    src/sas_core_py.cpp
    src/sas_robot_driver_py.cpp
    src/sas_modeling_py.cpp
)

target_link_libraries(_core PRIVATE marinholab::sas::core)
