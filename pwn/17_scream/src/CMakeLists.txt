# Please build with GCC Linux
cmake_minimum_required(VERSION 3.5)
project(pwn-scream)
add_executable(scream chall.c)
target_compile_options(scream PRIVATE -fPIE -fstack-protector-all)
target_link_options(scream PRIVATE -zrelro -znow)
