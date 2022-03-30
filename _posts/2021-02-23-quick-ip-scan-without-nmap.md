---
layout: post
title: Quick IP scan without nmap
tags: [python]
---

So nmap isn't always available to figure out what devices are up on your local network or where they may have moved too after you installed that new router but python is usually around.
This script will ping your local network for ip addresses. It is as basic as you can get and does not work on Windows. Some day I would like to make a better version of this, when I do, I will
link it back to here. In the meantime this maybe useful.

````python

#!/usr/bin/env python3
import socket
import platform
import subprocess

def get_ip():
    ip = ""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("10.255.255.255", 1))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def ping(host):
    param = '-n' if platform.system().lower()=='windows' else '-c'
    command = ['ping', '-t', '1', param, "1", host]
    return subprocess.call(command) == 0

if __name__ == "__main__":
    ip = get_ip()
    for i in range(253):
        tokens = ip.split(".")
        final_octet = tokens[-1]
        prefix = ".".join(tokens[0:3])
        new_final_octet = str(i+1)
        if final_octet != new_final_octet:
            ip_to_scan = prefix + "." + new_final_octet
            if ping(ip_to_scan):
                print("found {} {}".format(ip_to_scan, socket.gethostbyaddr(ip_to_scan)))
```
