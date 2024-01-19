#!/bin/sh

echo 'die "moo~";' > /flag
echo $GZCTF_FLAG >> /flag
chmod 444 /flag

unset GZCTF_FLAG

/usr/sbin/sshd -D
