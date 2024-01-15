# How to use this book

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

Here's what to do:

- In a web browser, open this link to the JupyterHub: <https://lore.atmos.albany.edu:8000>
This should bring you to a login screen. Use your standard UAlbany netid and password.
- You should now see a JupyterHub screen showing your home space on the DAES linux system.
- In a different browser window, navigate to the desired page of this book.
- Find the "Rocket ship" icon at top right. Hover over the icon and you should see several buttons appear.
- Click on the button that says `JupyterHub`.
- There may be a brief delay while a local copy of the notes is made for you (or updated) on the server.
- You should then see the notebook open and running live on the JupyterHub.
- **IMPORTANT** you need to manually *change the kernel* before things will run properly:
  - Find the `Kernel` menu
  - Select `Kernel --> Change kernel --> Python 3 Jan. 2024 Environment`
- You should then be able to run all the code without any trouble.

```{note}
Do this step every time! If you get errors trying to run any `import` statements, double check that you're using the `Python 3 Jan. 2024 Environment` kernel.
```

*UAlbany users, please let me know if things don't seem to be working correctly.*

## Public users: interact through a cloud-based Binder service

This will work well for many of the simple examples,
but some of the notes require more computational resources.
Binder is good for tinkering, but there is no easy way to save your work and come back to it.

To launch a notebook in Binder, hover over the "Rocket ship" icon at top right and click the `Binder` button. 

This will take you to an NSF-funded Binder service run by [Project Pythia](https://projectpythia.org).

## Google Colab users

Some users have reported success installing and running climlab on Google Colab. 
See [these instructions in the climlab docs](https://climlab.readthedocs.io/en/latest/installation.html#installing-on-google-colab). 

You would also need to clone the [source repository for this book on github][repo] into your Colab space. 
I'm not using Colab so I don't have step-by-step instructions for this, but the adventurous user might find this a good option.

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
[climlab]: https://github.com/climlab/climlab
[book]: https://brian-rose.github.io/ClimateLaboratoryBook/
[notebook]: https://jupyter-notebook.readthedocs.io/en/stable/
