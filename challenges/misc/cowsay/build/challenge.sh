#!/bin/sh

echo "Enter the name of the cowfile (e.g., default, sheep, dragon):"
read cowfile

echo "Enter a single-line message (press CTRL+D to skip):"
read message

echo "Enter a multiline message (press CTRL+D to finish):"
message_multiline=$(</dev/stdin)
echo "$message_multiline" | /usr/bin/cowsay -f $cowfile $message

exit 0
