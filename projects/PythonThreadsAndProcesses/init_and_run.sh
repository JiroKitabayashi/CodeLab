#!/bin/bash

# change directory to the shell file's directory
cd `dirname $0`

echo '---- initializing project ----'
# install package
pip install requests

# create log directory
mkdir -p log

# Grant execution permission and execute Python script
chmod +x multi_task_test.py


echo '---- Run test file ----'
python multi_task_test.py
