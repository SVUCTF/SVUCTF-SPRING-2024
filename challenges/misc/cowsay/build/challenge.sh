#!/bin/sh
read -p "Input cowfile:" cowfile
read -p "Input message:" message
/usr/bin/cowsay -f $cowfile $message
exit 0
