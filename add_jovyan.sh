#!/bin/bash -v
NB_USER=jovyan
NB_UID=2005
SHELL=/bin/bash
groupadd --gid ${NB_UID} ${NB_USER}
useradd --create-home --gid ${NB_UID} --no-log-init --uid ${NB_UID} ${NB_USER}
