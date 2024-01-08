#!/bin/sh
echo -n "Input cowfile:"
read cowfile
echo -n "Input message:"
read message
/usr/bin/cowsay -f $cowfile $message
exit 0
