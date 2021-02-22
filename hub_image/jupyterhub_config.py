# dummy for testing. Don't use this in production!
c.JupyterHub.authenticator_class = 'dummyauthenticator.DummyAuthenticator'

# launch with docker
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'

# we need the hub to listen on all ips when it is in a container
c.JupyterHub.hub_ip = '0.0.0.0'
# the hostname/ip that should be used to connect to the hub
# this is usually the hub container's name
c.JupyterHub.hub_connect_ip = 'jupyterhub_feb21'

# pick a docker image. This should have the same version of jupyterhub
# in it as our Hub.
c.DockerSpawner.image = 'phaustin/climbook:feb21'
notebook_dir = "/home/jovyan"
c.DockerSpawner.notebook_dir = notebook_dir

# tell the user containers to connect to our docker network
c.DockerSpawner.network_name = 'net_feb21'
c.DockerSpawner.volumes = {"jupyterhub-user-{username}": notebook_dir,
                            "/home/phil/repos/ClimateLaboratoryBook/shared_files": 
                            {"bind": '/home/jovyan/shared_files', "mode": "rw"},
                            "/home/phil/repos/ClimateLaboratoryBook/content":
                            {"bind": '/home/jovyan/content', "mode": "ro"}
                           }


# delete containers when the stop
c.DockerSpawner.remove = True
