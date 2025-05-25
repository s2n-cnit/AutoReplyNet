#!/bin/bash
tcpdump -i ens3 src 192.168.0.0/16 and dst 192.168.0.0/16 -w $1.pcap
