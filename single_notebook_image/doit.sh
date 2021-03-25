#!/bin/bash -v
conda activate base
conda env remove --name climlab
conda-lock -f environment.yml -p linux-64
conda env create --name climlab --file conda*linux*
conda activate climlab
pip install -r requirements_jupyter.txt
