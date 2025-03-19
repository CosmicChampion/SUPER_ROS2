cmake_minimum_required(VERSION 3.5)
project(perfect_drone_sim)
# Встановлення стандартів C та C++
if(NOT CMAKE_C_STANDARD)
  set(CMAKE_C_STANDARD 99)
endif()
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()
# Додаткові опції компіляції для GCC або Clang
if (CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic -Wnon-virtual-dtor -Woverloaded-virtual)
endif()
# Налаштування типу збірки
set(CMAKE_BUILD_TYPE "Release")
set(CMAKE_CXX_FLAGS_RELEASE "-O3 -Wall -g -fPIC")
add_compile_options(-DQT_NO_VERSION_TAGGING)
add_definitions(-DROOT_DIR=\"${CMAKE_CURRENT_SOURCE_DIR}/\")
# Встановлення шляху для пошуку пакетів (для CLion)
set(CMAKE_PREFIX_PATH ../../../../install)
# Пошук необхідних пакетів
find_package(PCL REQUIRED COMPONENTS common io)
find_package(pcl_conversions REQUIRED)
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(visualization_msgs REQUIRED)
find_package(marsim_render REQUIRED)
find_package(mars_quadrotor_msgs REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(Eigen3 REQUIRED)
find_package(OpenCV REQUIRED)
# Включення директорій для пошуку заголовкових файлів
include_directories(
  include
  SYSTEM
  ${PCL_INCLUDE_DIRS}
  ${EIGEN3_INCLUDE_DIRS}
)
# Встановлення залежностей
set(dependencies
  marsim_render
  rclcpp
  sensor_msgs
  mars_quadrotor_msgs
  std_msgs
  geometry_msgs
  nav_msgs
  visualization_msgs
  tf2_ros
  pcl_conversions
)
# Створення виконавчого файлу
add_executable(perfect_drone_node
  src/ros2_perfect_drone_node.cpp
)
# Зв'язування залежностей з виконавчим файлом
ament_target_dependencies(perfect_drone_node PUBLIC
  ${dependencies}
)
# Зв'язування сторонніх бібліотек
target_link_libraries(perfect_drone_node PUBLIC
  ${PCL_LIBRARIES}
  ${OpenCV_LIBRARIES}
  yaml-cpp
)
# Встановлення директорій для пошуку заголовкових файлів
target_include_directories(perfect_drone_node PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
)
# Інсталяція заголовкових файлів
install(
  DIRECTORY include/
  DESTINATION include
)
# Інсталяція виконавчого файлу
install(
  TARGETS perfect_drone_node
  EXPORT perfect_drone_node
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin
  INCLUDES DESTINATION include
  RUNTIME DESTINATION lib/${PROJECT_NAME}
)
# Інсталяція додаткових файлів (launch, rviz, meshes, config)
install(DIRECTORY
  launch
  rviz
  rviz2
  meshes
  config
  DESTINATION share/${PROJECT_NAME}/
)
# Експорт директорій з заголовковими файлами
ament_export_include_directories(include)
# Завершення пакету
ament_package()