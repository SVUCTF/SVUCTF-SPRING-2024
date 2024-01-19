#!/bin/sh

read -p "Enter the name of the cowfile (e.g., default, sheep, dragon):" cowfile
read -p "Enter the message:" message

/usr/bin/cowsay -f $cowfile $message
