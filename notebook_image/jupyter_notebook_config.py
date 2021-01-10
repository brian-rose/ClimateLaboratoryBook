# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import jupytext

c = get_config()  # noqa

c.NotebookApp.contents_manager_class = "jupytext.TextFileContentsManager"  # noqa
c.ContentsManager.preferred_jupytext_formats_save = "myst"  # noqa
c.ContentsManager.default_jupytext_formats = "ipynb,myst"  # noqa
c.ContentsManager.default_notebook_metadata_filter = (
    "all,-language_info,-toc,-latex_envs"
)

