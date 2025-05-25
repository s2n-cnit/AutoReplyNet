#!/bin/bash

if [ -z "$1" ]; then
	echo Missing output filename (without .pcap)
	exit 1
fi

tcpdump -i ens3 net 192.168.0.0/16 -w $1.pcap
