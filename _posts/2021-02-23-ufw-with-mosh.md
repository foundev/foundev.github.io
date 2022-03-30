---
layout: post
tags: [mosh, ufw]
---
<h1>Configuring UFW with Mosh support</h1>

[Mosh](https://blink.sh/) is kind of my secret weapon for working remotely but getting it configured to be allowed through the firewall is something I always seem to forget. So here is my
UFW script I use for new servers with mosh added in:


```
sudo ufw default deny incoming
sudo ufw allow 22/tcp
# this is hte part that allows mosh to work
sudo ufw allow 60000:61000/udp
sudo ufw enable
```


