FROM phaustin/base-image:jan09
USER ${NB_USER}

RUN mkdir -p ${HOME}/content

RUN echo "conda activate ${CONDA_ENV}" >> ${HOME}/.bashrc
COPY jupyter_notebook_config.py /etc/jupyter/

WORKDIR ${HOME}

CMD ["jupyterhub-singleuser"]
