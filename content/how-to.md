# How to use this book

*under construction*

Things are in flux...

There will be essentially **four different ways** to use the book:

**Option 1: Just read it!** The notes are designed to be fully self-explanatory and readable.
However to get the most of the material, you'll probably want to
*interact with the Python code* contained in the Jupyter notebooks.

There will be **three different ways** to run the Python code:

1. Through a public Binder *(currently broken -- working on it)*
This will work well for many of the simple examples,
but some of the notes require more computational resources.
Binder is good for tinkering, but there is no easy way to save your work and come back to it.

2. Through our private JupyterHub *(restricted to UAlbany users)*
This is the preferred route for UAlbany students. Anyone with login credentials
to our server will have a point-and-click interface to a completely interactive
version of the notes, and will be able to save their work and pull in new updates.

3. Run the code in your own Python environment.

Option 3 is open to anybody. You will need to use the conda package manager.

The first step is to clone the [source repository on github][repo].

Once you have the source repo,
the following commands will create a self-contained conda environment
with everything you need to run the notebooks (Mac, Linux and Windows).
From within the `ClimateLaboratoryBook` directory
in your favorite terminal, do this:

```
conda env create --file environment.yml
conda activate climlab-courseware
```

Then find all the Jupyter notebook `*.ipynb` files in `ClimateLaboratoryBook/content/courseware`

[repo]: https://github.com/brian-rose/ClimateLaboratoryBook
