#!/bin/sh

echo $GZCTF_FLAG > /flag
chmod 444 /flag

gunicorn main:app -b 0.0.0.0:5000 -w 1
