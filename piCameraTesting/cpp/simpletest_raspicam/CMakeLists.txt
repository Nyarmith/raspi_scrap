
cmake_minimum_required (VERSION 2.8) 
project (raspicam_test)

#tell where to look for raspicamConfig.cmake
set(raspicam_DIR "/usr/local/lib/cmake")

find_package(raspicam REQUIRED)
add_executable (simpletest_raspicam simpletest_raspicam.cpp)  
target_link_libraries (simpletest_raspicam ${raspicam_LIBS})

find_package(OpenCV REQUIRED core imgproc)
MESSAGE(STATUS "COMPILING OPENCV TESTS")
add_executable (simpletest_raspicam_cv simpletest_raspicam_cv.cpp)  
target_link_libraries (simpletest_raspicam_cv ${raspicam_CV_LIBS})

add_executable (centroid_stream centroid_stream.cpp)
target_link_libraries (centroid_stream ${raspicam_CV_LIBS})



