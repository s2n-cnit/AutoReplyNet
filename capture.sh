#!/bin/bash

if [ -z "$1" ]; then
	echo "Missing output filename"
	exit 1
fi

sudo tcpdump -i ens3 src net 192.168.0.0/16 and dst net 192.168.0.0/16 -w $1
