---
layout: post
---

<h1>New Minimal Dependency vimrc with ALE</h1>

<p>
I stumbled onto a good simple adjustment to my minimal config while trying to figure out a good vim setup for Java, Rust, and Go. Yes I know I can just use VSCode and everything will just work,
but for my home stuff I like to keep things relatively stripped down, maybe a few packages via homebrew to keep things up to date, but I no longer like to spend
oodles of time every time I log in running updates on a hundred different packages, vscode often feels like this to me, a chain of updates if I haven't logged in for awhile.
</p>

<h2>What is this ALE thing in the title</h2>

<p>
<a href="https://github.com/vim-syntastic/syntastic">Syntastic</a> was one of the old trusty packages I would install through vim packages and it worked a treat but it has moved on 
as many projects do and the page actually recommended <a href="https://github.com/dense-analysis/ale">ALE</a>. Ale provides a lot that syntastic didn't including completion and lsp support and
usually it needs little to no configuration (it picked up golps instantly). I played around with it at work and integrated some other plugins and was pretty happy. Later when I started working on something at home
I tried this more minimal version and still found it very pleasing to use. I have only installed <a href="https://github.com/vim-airline/vim-airline">airline</a> and ALE in my vim plugins.
</p>

<h2>actual vimrc</h2>

Key changes are:

* updated the find files script to match latest recommendation on fzy github page.
* added some ale specific config including my preferences for rust using rust-analyzer and rustfmt

```
let g:ale_completion_enabled = 1
let g:ale_sign_column_always = 1
let g:airline#extensions#ale#enabled = 1
let g:rustfmt_autosave = 1
let g:ale_linters = {
\ 'rust': ['analyzer'],
\}
let g:ale_fixers = {
 \   'rust': ['rustfmt'],
\}
set omnifunc=ale#completion#OmniFunc
nmap <silent> <C-k> <Plug>(ale_previous_wrap)
nmap <silent> <C-j> <Plug>(ale_next_wrap)

"minimal vimrc for basic editing
filetype plugin indent on
"pretty stuff
syntax on

:colorscheme industry

let mapleader = ","

"search for word vim
map <leader>n :execute "noautocmd vimgrep /" . expand("<cword>") . "/j " . vim_working_dir . "**/*." . expand("%:e")  <Bar> cw<CR>

"Remove all trailing whitespace by pressing F5
nnoremap <F5> :let _s=@/<Bar>:%s/\s\+$//e<Bar>:let @/=_s<Bar><CR>


function! FzyCommand(choice_command, vim_command)
  try
    let output = system(a:choice_command . " | fzy ")
  catch /Vim:Interrupt/
    " Swallow errors from ^C, allow redraw! below
  endtry
  redraw!
  if v:shell_error == 0 && !empty(output)
    exec a:vim_command . ' ' . output
  endif
endfunction

nnoremap <leader>e :call FzyCommand("ag . --silent -l -g ''", ":e")<cr>
nnoremap <leader>v :call FzyCommand("ag . --silent -l -g ''", ":vs")<cr>
nnoremap <leader>s :call FzyCommand("ag . --silent -l -g ''", ":sp")<cr>
"variable setting
"spell check for md files
autocmd BufRead,BufNewFile *.md setlocal spell spelllang=en_us
"default hide whitespace
set nolist
"tabs and other goods taken from web
set showmode
set hidden
set expandtab
set nowrap        " don't wrap lines
set tabstop=4     " a tab is four spaces
set shiftwidth=4  " number of spaces to use for autoindenting
set backspace=indent,eol,start
                  " allow backspacing over everything in insert mode
set autoindent    " always set autoindenting on
set copyindent    " copy the previous indentation on autoindenting
set shiftround    " use multiple of shiftwidth when indenting with '<' and '>'
set showmatch     " set show matching parenthesis
set ignorecase    " ignore case when searching
set smartcase     " ignore case if search pattern is all lowercase,
                  "    case-sensitive otherwise
set smarttab      " insert tabs on the start of a line according to
                  "    shiftwidth, not tabstop
set hlsearch      " highlight search terms
set incsearch     " show search matches as you type

set history=1000         " remember more commands and search history
set undolevels=1000      " use many muchos levels of undo
set wildignore=*.swp,*.bak,*.pyc,*.class
set title                " change the terminal's title
set visualbell           " don't beep
set noerrorbells         " don't beep

"backup files go away
set nobackup
set noswapfile
set clipboard=unnamed
"search for word working dir setting
let vim_working_dir = fnamemodify('.',':p:p')
"undo support
set undodir=$HOME/.vim/undo
set undolevels=1000
set undoreload=10000
"auto-reload buffers that have changed underneath
set autoread

if !has('gui_running')
  set t_Co=256
endif
```
