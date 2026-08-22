cmake_minimum_required(VERSION 3.8)
project(my_package)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
set(dependencies
  rclcpp
)
set(dependencies1
  rclcpp
  std_msgs
)

set(dependencies2
  rclcpp
  std_msgs
  sensor_msgs
)

add_executable(
  simple src/simple.cpp
)
ament_target_dependencies(simple ${dependencies})

add_executable(
   logger src/logger.cpp
)
ament_target_dependencies(logger ${dependencies1})

add_executable(
  pub src/publisher.cpp
)
ament_target_dependencies(pub ${dependencies1})
add_executable(
  sub src/subscriber.cpp
)
ament_target_dependencies(sub ${dependencies1})

add_executable(
  joy src/joy.cpp
)
ament_target_dependencies(joy ${dependencies2})

add_executable(
  turtle src/turtle_joy.cpp
)
ament_target_dependencies(turtle ${dependencies2})

install(TARGETS
  simple
  logger
  pub
  sub
  joy
  turtle
  DESTINATION lib/${PROJECT_NAME}
)
install(
  DIRECTORY 
  launch
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
