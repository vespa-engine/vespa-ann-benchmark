# Copyright Vespa.ai. Licensed under the terms of the Apache 2.0 license. See LICENSE in the project root.

if(NOT DEFINED VESPA_USE_SANITIZER)
  vespa_add_test(NAME ann_benchmark_test NO_VALGRIND COMMAND ${Python_EXECUTABLE} -m pytest WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR} ENVIRONMENT "GLIBC_TUNABLES=glibc.rtld.optional_static_tls=8000" DEPENDS vespa_ann_benchmark)
endif()
