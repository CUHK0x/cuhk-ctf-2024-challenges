#!/bin/bash
mkdir -p temp
g++ -O0 -c writeup/full.cpp -o temp/encryptor.o
g++ temp/encryptor.o -o public/encryptor
public/encryptor < in.txt