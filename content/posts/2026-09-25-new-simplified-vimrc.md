---
title: 'New simplified vimrc'
tags: [vim]
---

# New Simplified vimrc

Due to my use of AI I rarely drop to a text editor now. However, vim is wired into my muscle memory. Since a long time I have been carrying around the same base settings I started using in vim 7 or 6.x and honestly most of them are now the default, so I started stripping things out and after a few rounds my vimrc was nearly empty. So I asked, how about lsp support, ALE seems to have gotten less maintained, and it was always a bit quirky with autocomplete, so I loaded up vim-lsp and before you know it I had a functional editor useful for a pinch when I want to read some code and have an LSP server tell me the obvious problems. Behold, it is very simple and only requires the use of [vim-plug](https://github.com/junegunn/vim-plug) to get going. Enjoy:

```vimscript
all plug#begin()
" List your plugins here
Plug 'mattn/vim-lsp-settings'
Plug 'prabirshrestha/vim-lsp'
Plug 'prabirshrestha/asyncomplete.vim'
Plug 'prabirshrestha/asyncomplete-lsp.vim'
Plug 'preservim/nerdtree'
Plug 'ctrlpvim/ctrlp.vim'

call plug#end()
inoremap <expr> <Tab>   pumvisible() ? "\<C-n>" : "\<Tab>"
inoremap <expr> <S-Tab> pumvisible() ? "\<C-p>" : "\<S-Tab>"
inoremap <expr> <cr>    pumvisible() ? asyncomplete#close_popup() : "\<cr>"
set expandtab
set tabstop=4     " a tab is four spaces
set shiftwidth=4  " number of spaces to use for autoindenting
```
