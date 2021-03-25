# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import jupytext

c = get_config()  # noqa
c.NotebookApp.ip = '0.0.0.0'
c.NotebookApp.port = 8888
c.NotebookApp.open_browser = False
c.NotebookApp.token =  'be5b7760bdf178b9b52a8ace9c5ffe5eb51ecca6e195f82002e0d8468322b406'
c.NotebookApp.contents_manager_class = "jupytext.TextFileContentsManager"  # noqa
c.ContentsManager.preferred_jupytext_formats_save = "myst"  # noqa
c.ContentsManager.default_jupytext_formats = "ipynb,myst"  # noqa
c.ContentsManager.default_notebook_metadata_filter = (
    "all,-language_info,-toc,-latex_envs"
)

