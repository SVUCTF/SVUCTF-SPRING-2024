#!/bin/sh

echo $GZCTF_FLAG > /flag
chmod 444 /flag
unset GZCTF_FLAG

gunicorn main:app -b 0.0.0.0:5000
