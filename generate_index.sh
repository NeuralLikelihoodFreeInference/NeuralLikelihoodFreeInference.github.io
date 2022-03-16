#!/bin/bash

# generates the index.html file starting from the entries stored in the json file

python3 add_entries.py

# append the scripts
cat scripts.html >> index.html
