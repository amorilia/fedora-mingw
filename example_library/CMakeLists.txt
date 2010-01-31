cmake_minimum_required(VERSION 2.6)
project(test)

add_library(example example.c)

install(TARGETS example
        RUNTIME DESTINATION bin
        LIBRARY DESTINATION lib${LIB_SUFFIX}
        ARCHIVE DESTINATION lib${LIB_SUFFIX}
)

install(FILES example.h
        DESTINATION include)

enable_testing()
add_executable(runtest runtest.c)
target_link_libraries(runtest example)
add_test(test runtest${CMAKE_EXECUTABLE_SUFFIX})
