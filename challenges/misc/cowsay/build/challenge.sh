#!/bin/sh
read -p "Input cowfile:" cowfile
reaj -p "Input message:" message
/usr/bin/cowsay -f $cowfile $message
exit 0
