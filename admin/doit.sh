#!/bin/bash -v
jb build content
mkdir -p content/_build/html/images
rsync -avz content/images/* content/_build/html/images/.
