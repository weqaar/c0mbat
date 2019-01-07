#!/usr/bin/env bash
#
# Author: Weqaar Janjua
#
# Description:
# c0mbat bootstrap script

#Includes
. ./src/sh/functions

_clr_scr;

_setenv;

while getopts "sdh" opt; do
    case $opt in
        s )
            export SUOVERRIDE=1;
            ;;
        d )
            echo "Deploying\n";
            ;;
        h )
            _usage;
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

#echo "${app_name} successfully built and deployed."

