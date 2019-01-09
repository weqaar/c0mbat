#!/usr/bin/env bash
#
# Author: Weqaar Janjua
#
# Description:
# c0mbat bootstrap script

#Includes
. ./src/sh/functions

#Variables
_PROJECT=c0mBat
_VERSION=3.7alpha
_PIPLOG=${_PROJECT}_pip.log

_setenv;

if [ -z "$1" ]
then
    echo "Invalid option: -$OPTARG" 2>/dev/null;
    _usage;
    exit 1;
fi

while getopts "shrid:" opt; do
    case $opt in
        s )
            export SUOVERRIDE=1;
            ;;
        h )
            _usage;
            ;;
        r )
            pipreqs --force --use-local .
            ;;
        i )
            echo "Install python deps with pip..."
            if [ `id -u` -eq 0 ]; then
                pip install -r requirements.txt >>${_PIPLOG} 2>&1
            else
                sudo pip install -r requirements.txt >>${_PIPLOG} 2>&1
            fi
            echo "Done."
            ;;
        d )
            [ -d ${OPTARG} ] || mkdir -p ${OPTARG}
            if [ $? -eq 0 ]; then
                cp -r src/* ${OPTARG}
                mkdir ${OPTARG}/docs
                cp -r docs/build/* ${OPTARG}/docs
                echo "Install python deps with pip..."
                if [ `id -u` -eq 0 ]; then
                    pip install -r requirements.txt >>${_PIPLOG} 2>&1
                else
                    sudo pip install -r requirements.txt >>${_PIPLOG} 2>&1
                fi
                echo "\n${_PROJECT} ver.${_VERSION} installed in ${OPTARG}\n"
                echo "Read documentation under ${OPTARG}/docs\n"
            else
                echo "directory " ${OPTARG} "is not writable, exiting."
            fi
            ;;
        \? )
            echo "Invalid option: -$OPTARG" 2>/dev/null;
            _usage;
            exit 1;
            ;;
        esac
    done
shift $(( OPTIND -1 ))

_check_euid;
if [ $? -eq ${FALSE} ]; then
    echo "Should not run as root (uid 0), please run as a non-priviledged user.";
    exit 0;
fi

_check_dir_writable ${PRJROOT};

#EOF
