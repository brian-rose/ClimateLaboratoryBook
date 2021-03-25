FROM phaustin/base-image:jan09
USER ${NB_USER}

RUN mkdir -p ${HOME}/shared_files
RUN mkdir -p ${HOME}/content
RUN mkdir -p ${HOME}/work

USER root
RUN cd /home/jovyan
RUN chown -R jovyan work
RUN chgrp -R jovyan work

USER ${NB_USER}


RUN echo "conda activate ${CONDA_ENV}" >> ${HOME}/.bashrc
COPY jupyter_notebook_config.py /etc/jupyter/

WORKDIR ${HOME}

CMD ["jupyterhub-singleuser"]
