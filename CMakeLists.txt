# Copyright Vespa.ai. Licensed under the terms of the Apache 2.0 license. See LICENSE in the project root.
cmake_minimum_required(VERSION 3.20 FATAL_ERROR)

list(PREPEND CMAKE_PREFIX_PATH "/opt/vespa" "/opt/vespa-deps")

list(APPEND CMAKE_MODULE_PATH
     "$ENV{HOME}/vespa/share/cmake"
     "/opt/vespa/share/cmake"
     "$ENV{HOME}/share/cmake/Modules"
     "/opt/vespa-deps/share/cmake/Modules"
)
message("-- CMAKE_MODULE_PATH is ${CMAKE_MODULE_PATH}")
SET_PROPERTY(GLOBAL PROPERTY TARGET_SUPPORTS_SHARED_LIBS TRUE)
find_package(vespa 8.0 REQUIRED)
message("VESPA_CMAKECONFIG_DIR is ${VESPA_CMAKECONFIG_DIR}")
include(${VESPA_CMAKECONFIG_DIR}/functions.cmake)
include(${VESPA_CMAKECONFIG_DIR}/default_build_settings.cmake)
vespa_detect_build_platform()
message("-- Vespa build platform is ${VESPA_OS_DISTRO} ${VESPA_OS_DISTRO_VERSION}")
vespa_use_default_cxx_compiler()

project(vespa-ann-benchmark CXX C)
vespa_use_default_vespa_unprivileged()
vespa_use_default_cmake_install_prefix()
include(GNUInstallDirs)
vespa_use_default_vespa_deps_prefix()
vespa_use_default_cmake_prefix_path()

SET(CMAKE_FIND_PACKAGE_SORT_ORDER NATURAL)
SET(CMAKE_FIND_PACKAGE_SORT_DIRECTION DEC)

find_package(Threads REQUIRED)

vespa_use_default_build_settings()

list(PREPEND CMAKE_BUILD_RPATH ${VESPA_HOME}/lib64)
if(NOT "${CMAKE_INSTALL_PREFIX}" STREQUAL "${VESPA_HOME}")
  list(PREPEND CMAKE_INSTALL_RPATH ${VESPA_HOME}/lib64)
endif()

# allows import of project in CLion on OSX
if (${CMAKE_SYSTEM_NAME} MATCHES "Darwin")
    set(CMAKE_THREAD_LIBS_INIT "-lpthread")
endif()

if (( ${VESPA_OS_DISTRO} STREQUAL "almalinux" OR
      ${VESPA_OS_DISTRO} STREQUAL "centos" OR
      ${VESPA_OS_DISTRO} STREQUAL "ol" OR
      ${VESPA_OS_DISTRO} STREQUAL "rhel" OR
      ${VESPA_OS_DISTRO} STREQUAL "rocky") AND
    ( ${VESPA_OS_DISTRO_VERSION} VERSION_GREATER_EQUAL 8 AND
      NOT (${VESPA_OS_DISTRO_VERSION} VERSION_GREATER_EQUAL 9)))
  set(VESPA_PYTHON_VERSION_SPEC "3.11...<3.12")
else()
  set(VESPA_PYTHON_VERSION_SPEC "3.6")
endif()
find_package(Python ${VESPA_PYTHON_VERSION_SPEC} COMPONENTS Interpreter Development REQUIRED)
find_package(pybind11 CONFIG REQUIRED)

include(${VESPA_CMAKECONFIG_DIR}/build_settings.cmake)
include(${VESPA_CMAKECONFIG_DIR}/cxx_settings.cmake)

# Enable CTest unit testing
enable_testing()

add_subdirectory(ann_benchmark)

# Create module targets with name ${MODULE}+module depending on every target defined within that module
__create_module_targets(TARGETS "module")

# Create module targets with name ${MODULE}+test depending on every test target defined within that module
__create_module_targets(TEST_TARGETS "test")

# Create module targets with name ${MODULE}+source depending on every source target defined within that module
__create_module_targets(SOURCE_TARGETS "source")

# Create module targets with name ${MODULE}+object depending on every object target defined within that module
__create_module_targets(OBJECT_TARGETS "object")

# Create module source dependencies
__create_module_source_dependencies()
