#!/usr/bin/env zsh

setopt ERR_EXIT

gcc -std=gnu99 -E kernel3.c -lm -o debug.txt

cat debug.txt | egrep -v '^\#' | sed -e 's/{/{\n/g' | sed -e 's/}/}\n/g' | sed -e 's/;/;\n/g' | egrep -v '^$' > debug.c
#cat kernel3.i | egrep -v '^\#'  | sed 's/;/;\n/' > debug.c

gcc -g -std=gnu99 debug.c -lm -o debug.exe

ddd debug.exe

