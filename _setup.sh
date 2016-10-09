#!/bin/sh -eu

if [ ! -d modules ]
then
    mkdir modules
fi

if [ ! -d modules/ansible-go-module ]
then
    git clone https://github.com/suzuki-shunsuke/ansible-go-module modules/ansible-go-module
fi

if [ ! -d _roles ]
then
    mkdir _roles
fi

ansible-galaxy install -r roles.yml
