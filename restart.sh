#!/bin/sh
ret=`ps -ef | grep main  | awk '{print $2}' | xargs kill -9`
nohup python3 main.py > ./nohup.out 2>&1 &