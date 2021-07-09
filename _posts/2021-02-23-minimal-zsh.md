---
layout: post
title: minimal zsh prompt that is useful
tags: [ zsh ]
---
So oh-my-zsh is great but I like to do as much as I can on my own So I came up with a basic zsh prompt that gives me enough 
information to know what server I am on and what directory I am in (also git branch)

Enjoy

```sh

autoload -Uz vcs_info
precmd() { vcs_info }

# Format the vcs_info_msg_0_ variable
zstyle ':vcs_info:git:*' formats ' %b'
setopt PROMPT_SUBST
# export PATH=$HOME/bin:/usr/local/bin:$PATH
# 
# %(?.√.?%?)    if return code ? is 0, show √, else show ?%?
# %?    exit code of previous command
# %1~   current working dir, shortening home to ~, show only last 1 element
# %#    # with root privileges, % otherwise
# %B %b start/stop bold
# %F{...}   text (foreground) color, see table
# %f    reset to default textcolor
export PROMPT='%(?.%F{green}√.%F{red}?%?)%f %B%F{240}%1~%f%b@%F{184}%m%f %F{green}${vcs_info_msg_0_}%f %# '

export PATH=$PATH:$HOME/go/bin:$HOME/.cargo/bin
```
