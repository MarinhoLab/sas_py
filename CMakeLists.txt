# https://pybind11.readthedocs.io/en/stable/compiling.html
cmake_minimum_required(VERSION 3.16)

if(WIN32)
    set(CMAKE_TOOLCHAIN_FILE C:/vcpkg/scripts/buildsystems/vcpkg.cmake)
endif()

project(marinholab_sas_py LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# _core is self-contained: marinholab_sas_core is built as a static library
# and linked into _core, so the extension module has no dependency on a
# separately installed marinholab_sas_core shared library.
#
# dqrobotics itself is dynamically linked on every platform: sas_cpp links
# the installed shared library (libdqrobotics.so / dqrobotics.dll) located
# by find_library. That library must therefore ship inside the wheel so the
# installed package is importable without a separate dqrobotics install:
# - Windows: a DLL in the same directory as a .pyd is always resolved at
#   import time, and setuptools bundles auxiliary native libraries next to
#   an extension into the wheel. Copy dqrobotics.dll next to _core.pyd.
# - Linux: no manual copy — `auditwheel repair` (in the workflow) detects
#   libdqrobotics.so as a NEEDED dependency and bundles it into the wheel.
# - macOS (not in the CI matrix): the installed dylib is linked by its
#   absolute install name, which works on the building machine; bundling
#   it in place would additionally need install_name_tool rewriting.
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

if(WIN32)
    # The import library (dqrobotics.lib) satisfies the link; the runtime
    # dqrobotics.dll lives in <prefix>/bin and must be bundled next to
    # _core.pyd. CMAKE_PREFIX_PATH points at the dqrobotics install prefix
    # (set with -DCMAKE_PREFIX_PATH, or as an environment variable); the
    # vcpkg toolchain prepends its own prefix to the same variable for
    # Eigen3, so both coexist.
    find_file(DQROBOTICS_RUNTIME_LIB
        NAMES dqrobotics.dll
        PATH_SUFFIXES bin
        NO_DEFAULT_PATH
        HINTS "${CMAKE_PREFIX_PATH}"
              ENV CMAKE_PREFIX_PATH)
    if(NOT DQROBOTICS_RUNTIME_LIB)
        message(FATAL_ERROR "dqrobotics.dll not found "
                            "(looked in <CMAKE_PREFIX_PATH>/bin); "
                            "the wheel would not be importable")
    endif()
    add_custom_command(TARGET _core POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy_if_different
            "${DQROBOTICS_RUNTIME_LIB}"
            "$<TARGET_FILE_DIR:_core>"
        COMMENT "Bundling dqrobotics.dll next to _core")
elseif(APPLE)
    find_file(DQROBOTICS_RUNTIME_LIB
        NAMES libdqrobotics.dylib dqrobotics.dylib
        PATH_SUFFIXES lib
        NO_DEFAULT_PATH
        HINTS "${CMAKE_PREFIX_PATH}"
              ENV CMAKE_PREFIX_PATH
              /usr/local
              /opt/homebrew)
    if(DQROBOTICS_RUNTIME_LIB)
        set_target_properties(_core PROPERTIES
            BUILD_WITH_INSTALL_RPATH ON
            INSTALL_RPATH "@loader_path")
        add_custom_command(TARGET _core POST_BUILD
            COMMAND ${CMAKE_COMMAND} -E copy_if_different
                "${DQROBOTICS_RUNTIME_LIB}"
                "$<TARGET_FILE_DIR:_core>"
            COMMENT "Bundling the dqrobotics dylib next to _core")
    endif()
endif()
