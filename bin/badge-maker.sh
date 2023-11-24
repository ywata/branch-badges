#!/usr/bin/env bash

if [ $# -gt 0 ]; then
    git branch -r --sort=committerdate | bin/badge-markdown.py > $1
fi    
