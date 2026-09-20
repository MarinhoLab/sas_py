# https://pybind11.readthedocs.io/en/stable/compiling.html
cmake_minimum_required(VERSION 3.16)

if(WIN32)
    set(CMAKE_TOOLCHAIN_FILE C:/vcpkg/scripts/buildsystems/vcpkg.cmake)
endif()

project(marinholab_sas_py LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# The wheel build emits _core into an "extdir" given by setup.py as
# CMAKE_LIBRARY_OUTPUT_DIRECTORY (single-config generators) or
# CMAKE_LIBRARY_OUTPUT_DIRECTORY_RELEASE (MSVC multi-config). On Windows the
# shared dqrobotics library is a runtime (DLL) target, which MSVC places in
# the RUNTIME output directory, so mirror the LIBRARY output dir into the
# RUNTIME output dir. The runtime library (dqrobotics.dll /
# libdqrobotics.so / libdqrobotics.dylib) is therefore built next to _core,
# and setuptools bundles auxiliary native libraries next to an extension
# into the wheel — the installed package is importable without a separate
# dqrobotics install.
if(WIN32)
    if(CMAKE_LIBRARY_OUTPUT_DIRECTORY_RELEASE)
        set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_RELEASE
            "${CMAKE_LIBRARY_OUTPUT_DIRECTORY_RELEASE}")
    endif()
    if(CMAKE_LIBRARY_OUTPUT_DIRECTORY)
        set(CMAKE_RUNTIME_OUTPUT_DIRECTORY
            "${CMAKE_LIBRARY_OUTPUT_DIRECTORY}")
    endif()
endif()

# dqrobotics is built in-tree and dynamically linked in every build
# (same structure as working-needlemanipulation, which builds it in-tree).
# BUILD_SHARED_LIBS is a cache variable read by each subproject's option():
#   ON  -> dqrobotics builds the shared library
#   OFF -> marinholab_sas_core builds as a static library that is linked
#          into _core, so the extension module has no dependency on a
#          separately installed marinholab_sas_core shared library.
set(BUILD_SHARED_LIBS ON CACHE BOOL "" FORCE)

add_subdirectory(submodules/dqrobotics/cpp)

set(MARINHO_LAB_SAS_CORE_BUILD_EXAMPLES OFF CACHE BOOL "" FORCE)
set(BUILD_SHARED_LIBS OFF CACHE BOOL "" FORCE)

add_subdirectory(submodules/sas_cpp)

set(PYBIND11_FINDPYTHON ON)
add_subdirectory(submodules/pybind11)

pybind11_add_module(_core MODULE
    src/sas_core_py.cpp
    src/sas_robot_driver_py.cpp
)

target_link_libraries(_core PRIVATE marinholab::sas::core)

# Find the dqrobotics runtime library bundled next to _core at import time:
# - Windows: a DLL in the same directory as a .pyd is always resolved.
# - macOS: the dylib carries an @rpath install name; @loader_path finds the
#   copy in the installed package.
# - Linux: auditwheel repair (in the workflow) rewrites the NEEDED entry and
#   bundles libdqrobotics.so into the manylinux wheel.
if(APPLE)
    set_target_properties(_core PROPERTIES
        BUILD_WITH_INSTALL_RPATH ON
        INSTALL_RPATH "@loader_path")
elseif(UNIX)
    set_target_properties(_core PROPERTIES
        BUILD_WITH_INSTALL_RPATH ON
        INSTALL_RPATH "$ORIGIN")
endif()
