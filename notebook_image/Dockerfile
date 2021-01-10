FROM phaustin/base-image:jan09
USER ${NB_USER}

RUN mkdir -p ${HOME}/work
RUN mkdir -p ${HOME}/work/sat_data
RUN mkdir -p ${HOME}/work/a301_lib
RUN mkdir -p ${HOME}/work/data_share
RUN mkdir -p ${HOME}/work/sat_lib

RUN echo "conda activate ${CONDA_ENV}" >> ${HOME}/.bashrc
COPY jupyter_notebook_config.py /etc/jupyter/

WORKDIR ${HOME}/work

CMD ["jupyterhub-singleuser"]
