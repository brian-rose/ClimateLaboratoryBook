# How to use this book

*under construction*

I wrote this book with a strong emphasis on *reproducibility* of the content.
For example, most of the figures in the notes are generated interactively,
often using data pulled from public servers. This means that readers are able
to reproduce all the results and use the code as starting points
for their own investigations.

In some cases the code to produce figures and animations may be hidden by default,
but you will always be able to click to reveal the Python code, and/or
open the underlying [Jupyter notebook][notebook] with all the details.

The notes are designed to be fully self-explanatory and readable.
However to get the most of the material, you'll probably want to
*interact with the Python code* contained in the Jupyter notebooks.

There are several different ways to do this.

## UAlbany users: interact through our dedicated JupyterHub

This is the preferred route for UAlbany students. Anyone with login credentials
to our server will have a point-and-click interface to a completely interactive
version of the notes, and will be able to save their work and pull in new updates.

Here are some basic instructions *(subject to change as we work out some kinks...)*:

- In a web browser, open this link to the JupyterHub: <https://lore.atmos.albany.edu:8000>
This should bring you to a login screen. Use your standard UAlbany netid and password.
- You should now see a JupyterHub screen showing your home space on the DAES linux system.
- In a different browser window, navigate to the desired page of this book.
- Click on the button that says `Interact (UAlbany only)`.
- There may be a brief delay while a local copy of the notes is made for you (or updated) on the server.
- You should then see the notebook open and running live on the JupyterHub.
- **IMPORTANT** you need to manually *change the kernel* before things will run properly:
  - Find the `Kernel` menu
  - Select `Kernel --> Change kernel --> ATM415: Python 3`
- You should then be able to run all the code without any trouble.

*UAlbany users, please let me know if things don't seem to be working correctly.*

### TEMPORARY TEST

Link to some other JupyterHub instances:
- <https://reed.atmos.albany.edu:8000>
- <https://ash.atmos.albany.edu:8000>
- <https://rainier.atmos.albany.edu:8000>


## Public users: interact through a cloud-based Binder service

*(currently broken -- working on it)*

This will work well for many of the simple examples,
but some of the notes require more computational resources.
Binder is good for tinkering, but there is no easy way to save your work and come back to it.

## Anyone: run the code in your own Python environment

You will need the following:

- The [conda package manager](https://docs.conda.io/en/latest/)
- Basic knowledge of [version control with git](https://git-scm.com)
- Basic knowledge of [Jupyter notebooks][notebook]

The first step is to clone the [source repository for this book on github][repo].

Once you have the source repo, the following commands will create a self-contained
[conda environment](https://docs.conda.io/projects/conda/en/latest/user-guide/concepts/environments.html)
with everything you need to run the notebooks (Mac, Linux and Windows),
including the specialized [climlab toolkit][climlab].

From within the `ClimateLaboratoryBook` directory in your favorite terminal, do this:

```
conda env create --file environment.yml
conda activate climlab-courseware
```

Then find all the Jupyter notebook `*.ipynb` files in `ClimateLaboratoryBook/content/courseware`

You may find it useful to do all your work in a separate git branch,
and leave your `main` branch untouched so you can keep it up to date with
the source repository.

[repo]: https://github.com/brian-rose/ClimateLaboratoryBook
[climlab]: https://github.com/brian-rose/climlab
[book]: https://brian-rose.github.io/ClimateLaboratoryBook/
[notebook]: https://jupyter-notebook.readthedocs.io/en/stable/
