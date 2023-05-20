#!/bin/bash

# 查找所有正在运行的Python进程，并提取它们的PID列表
pids=$(ps -ef | grep python | grep -v grep | awk '{print $2}')

# 将PID列表转换为数组，并遍历数组以逐个终止进程
for pid in $(echo $pids); do
    echo "Killing PID $pid"
    sudo kill -9 $pid
done
