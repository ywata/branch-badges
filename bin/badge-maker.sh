#!/usr/bin/env bash

if [ $# -gt 2 ]; then
    repo=$1
    badge_format=$2
    shift 2
    echo "${repo} ${badge_format} $@"
    git branch -r --sort=committerdate | bin/badge-markdown.py markdown --repository ${repo} --badge-format ${badge_format} --workflows $@
fi    
