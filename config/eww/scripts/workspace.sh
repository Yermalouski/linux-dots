#!/bin/bash

qtile cmd-obj -o group -f info | python3 -c "
import sys, ast
data = ast.literal_eval(sys.stdin.read())  # Safely parse Python dict
print(data['name'])  # Extract and print the workspace name
"
