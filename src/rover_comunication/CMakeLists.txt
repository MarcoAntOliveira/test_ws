cmake_minimum_required(VERSION 3.8)
project(rover_comunication)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)


add_executable(motor_test src/motor_test.cpp)
ament_target_dependencies(motor_test rclcpp)

ament_package()
