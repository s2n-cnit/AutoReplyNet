#!/bin/bash
tcpdump -i ens3 net 192.168.0.0/16 -w $1.pcap
