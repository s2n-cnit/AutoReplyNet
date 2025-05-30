#!/bin/bash

if [ -z "$1" ]; then
	echo "Missing input filename"
	exit 1
fi

if [ -z "$2" ]; then
	echo "Missing packet direction (src or dst)"
	exit 2
fi

tshark -r $1 -T fields -e ip.$2 > tmp
sed '/^$/d' tmp | sort | uniq -c
#rm tmp
