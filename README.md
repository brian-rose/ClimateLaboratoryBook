# The Climate Laboratory

[![DOI](https://zenodo.org/badge/231609808.svg)](https://zenodo.org/badge/latestdoi/231609808)
![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/brian-rose/ClimateLaboratoryBook/deploy-book/main?logo=github&style=for-the-badge)

***A hands-on approach to climate physics and climate modeling***

**By [Brian E. J. Rose][brian], University at Albany**

## About the book

This book is powered by [JupyterBook][jupyterbook],
and aims to be all of the following:
- **self-reproducing** *(most figures are self-generating in the notebooks)*
- **free** and **open** *(permissive license, sources and content available through github)*
- **interactive** *(integration with JupyterHub and Binder will allow readers to run and modify code examples)*
- a **living document** *(content will continue to evolve, and collaboration is welcome)*

The material is mostly based on lecture notes for
[ENV 415: Climate Laboratory][env415] and [ATM 623: Climate Modeling][atm623]
at the [University at Albany][ualbany].

[To view the book online, go here][book].
The JupyterBook source and all book content (mostly [Jupyter Notebook][notebook] files)
are all in [this github repository][repo].

Much of the content is made possible by [climlab][climlab], an open-source
Python toolkit for interactive, process-oriented climate modeling.
[Brian Rose][brian] is the principle developer of climlab as well as the author of this book.

The contents of this book are licensed for free and open consumption under the following license:
[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)

## How to contribute or modify the book

The [source repository on github][repo] contains everything you need to build your own local version of the book.

From a local clone of the source, set up a self-contained conda environment with
```
conda env create --file environment.yml
conda activate climlab-courseware
```
This environment contains all dependencies for *both* building the book and running all the code in the book.

To build a local copy of the book, do this from the source root
```
jupyter-book build .
```

You will then find the built book in `_build/html/`, which you can open in a web browser e.g. with
```
open _build/html/index.html
```

Note that building the book creates the html from the `*.md` and `*.ipynb` sources, but does ***not*** re-run the notebooks. When building the book, we assume that all notebooks are already up-to-date!
*(You can change this behavior by modifying the `execute_notebooks` flag in `_config.yml`, but beware that some of the notebooks take a very long time to execute.)*

Anyone is welcome to suggest edits or improvements by opening pull requests on the [github repository][repo]. If you are editing any code in a notebook, please make sure you execute the modified notebook cleanly before submitting the PR.

## How is the book published

[The book][book] is just the rendered html that results from running `jupyter-book build`. Currently I use the [ghp-import][ghp-import] tool to copy the built html to the `gh-pages` branch on [github][repo].

See the [JupyterBook docs][jbook-publish] for more info on this.


[brian]: http://www.atmos.albany.edu/facstaff/brose/index.html
[env415]: http://www.atmos.albany.edu/facstaff/brose/classes/ENV415_Spring2018/
[atm623]: http://www.atmos.albany.edu/facstaff/brose/classes/ATM623_Spring2019/
[ualbany]: https://www.albany.edu
[about]: /about
[jupyterbook]: https://jupyterbook.org
[climlab]: https://github.com/brian-rose/climlab
[book]: https://brian-rose.github.io/ClimateLaboratoryBook/
[repo]: https://github.com/brian-rose/ClimateLaboratoryBook
[notebook]: https://jupyter-notebook.readthedocs.io/en/stable/
[ghp-import]: https://github.com/c-w/ghp-import
[jbook-publish]: https://jupyterbook.org/publish/gh-pages.html
