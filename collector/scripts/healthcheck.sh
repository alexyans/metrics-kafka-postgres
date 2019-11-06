#!/bin/bash

# crude healthcheck that checks the number of running python processes
PYTHON_PROCESS_COUNT = $(ps -e | grep python | wc -l)

if [$PYTHON_PROCESS_COUNT -eq 0]
then
    exit 1
else
    exit 0
fi

