#!/bin/sh

echo 'die "moo~";' > /flag
echo $GZCTF_FLAG >> /flag
chmod 444 /flag

unset GZCTF_FLAG

gunicorn app:app -b 0.0.0.0:5000
