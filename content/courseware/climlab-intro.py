# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.8.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown] slideshow={"slide_type": "slide"}
# # Building simple climate models using climlab
#
# This notebook is part of [The Climate Laboratory](https://brian-rose.github.io/ClimateLaboratoryBook) by [Brian E. J. Rose](http://www.atmos.albany.edu/facstaff/brose/index.html), University at Albany.

# %% [markdown]
# ____________
# <a id='section1'></a>
#
# ## 1. Introducing climlab
# ____________
#
#
# ## About climlab
#
# climlab is a specialized python package for process-oriented climate modeling.
#
# It is based on a very general concept of a model as a collection of individual, 
# interacting processes. climlab defines a base class called `Process`, which
# can contain an arbitrarily complex tree of sub-processes (each also some 
# sub-class of `Process`). Every climate process (radiative, dynamical, 
# physical, turbulent, convective, chemical, etc.) can be simulated as a stand-alone
# process model given appropriate input, or as a sub-process of a more complex model. 
# New classes of model can easily be defined and run interactively by putting together an
# appropriate collection of sub-processes.
#
# climlab is an open-source community project. The latest code can always be found on github:
#
# https://github.com/brian-rose/climlab
#
# ## Installing climlab
#
# If you've followed [these instructions from the Climate Laboratory book](https://brian-rose.github.io/ClimateLaboratoryBook/how-to.html), then you should be all set -- climlab is automatically installed as part of the suite of tools used in [The Climate Laboratory](https://brian-rose.github.io/ClimateLaboratoryBook).
#
# If you are maintaining your own Python installation (e.g. on a personal laptop), you can always install climlab by doing
#
# ```
# conda install -c conda-forge climlab
# ```

# %% [markdown]
# ____________
# <a id='section2'></a>
#
# ## 2. Using climlab to implement the zero-dimensional energy balance model
# ____________
#

# %% [markdown]
# ### The model equation (recap)
#
# Recall that we have worked with a zero-dimensional Energy Balance Model
#
# $$ C \frac{dT_s}{dt} = (1-\alpha) Q - \tau \sigma T_s^4 $$ 

# %% [markdown]
# Here we are going to implement this exact model using climlab.
#
# Yes, we have already written code to implement this model, but we are going to repeat this effort here as a way of learning how to use climlab.
#
# There are tools within climlab to implement much more complicated models, but the basic interface will be the same.

# %% [markdown]
# ### Create the state variables for the model

# %%
#  As usual, we start with some import statements.
# %matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
import climlab  # import climlab just like any other package

# %%
# create a zero-dimensional domain with a single surface temperature
state = climlab.surface_state(num_lat=1,  # a single point
                              water_depth = 100.,  # 100 meters slab of water (sets the heat capacity)
                             )
print(state)

# %% [markdown]
# Here we have created a dictionary called `state` with a single item called `Ts`:

# %%
print(state['Ts'])

# %% [markdown]
# This dictionary holds the state variables for our model -- which is this case is a single number!  It is a **temperature in degrees Celsius**.

# %% [markdown]
# For convenience, we can access the same data as an attribute (which lets us use tab-autocomplete when doing interactive work):

# %%
print(state.Ts)

# %% [markdown]
# It is also possible to see this `state` dictionary as an `xarray.Dataset` object:

# %%
climlab.to_xarray(state)

# %% [markdown]
# ### Create the subcomponents of the model

# %%
#  create the longwave radiation process
olr = climlab.radiation.Boltzmann(name='OutgoingLongwave',
                                  state=state, 
                                  tau = 0.612,
                                  eps = 1.,
                                  timestep = 60*60*24*30.)
#  Look at what we just created
print(olr)

# %%
#  create the shortwave radiation process
asr = climlab.radiation.SimpleAbsorbedShortwave(name='AbsorbedShortwave',
                                                state=state, 
                                                insolation=341.3, 
                                                albedo=0.299,
                                                timestep = 60*60*24*30.)
#  Look at what we just created
print(asr)

# %% [markdown]
# ### Create the model by coupling the subcomponents

# %%
#  couple them together into a single model
ebm = climlab.couple([olr,asr])
#  Give the parent process name
ebm.name = 'EnergyBalanceModel'
#  Examine the model object
print(ebm)

# %% [markdown]
# The object called `ebm` here is the entire model -- including its current state (the temperature `Ts`) as well as all the methods needed to integrated forward in time!

# %% [markdown]
# The current model state, accessed two ways:

# %%
print(ebm.state)

# %%
print(ebm.Ts)

# %% [markdown]
# ### Take a single timestep forward

# %% [markdown]
# Here is some internal information about the timestep of the model:

# %%
print(ebm.time['timestep'])
print(ebm.time['steps'])

# %% [markdown]
# This says the timestep is 2592000 seconds (30 days!), and the model has taken 0 steps forward so far.

# %% [markdown]
# To take a single step forward:

# %%
ebm.step_forward()

# %%
ebm.Ts

# %% [markdown]
# The model got colder!
#
# To see why, let's look at some useful diagnostics computed by this model:

# %%
ebm.diagnostics

# %% [markdown]
# This is another dictionary, now with two items. They should make sense to you.
#
# Just like the `state` variables, we can access these `diagnostics` variables as attributes:

# %%
ebm.OLR

# %%
ebm.ASR

# %% [markdown]
# So why did the model get colder in the first timestep?
#
# What do you think will happen next?

# %% [markdown]
# ____________
# <a id='section3'></a>
#
# ## 3. Run the zero-dimensional EBM out to equilibrium
# ____________

# %% [markdown]
# Let's look at how the model adjusts toward its equilibrium temperature.
#
# ### Exercise
#
# - Using a `for` loop, take 500 steps forward with this model
# - Store the current temperature at each step in an array
# - Make a graph of the temperature as a function of time

# %%

# %% [markdown]
# ____________
# <a id='section4'></a>
#
# ## 4. A climate change scenario 
# ____________

# %% [markdown]
# ### Description of the scenario
#
# Suppose we want to investigate the effects of a small decrease in the transmissitivity of the atmosphere `tau`. 
#
# Previously we used the zero-dimensional model to investigate a **hypothetical climate change scenario** in which:
# - the transmissitivity of the atmosphere `tau` decreases to 0.57
# - the planetary albedo increases to 0.32

# %% [markdown]
# ### Implement the scenario in climlab
#
# How would we do that using `climlab`?
#
# Recall that the model is comprised of two sub-components:

# %%
for name, process in ebm.subprocess.items():
    print(name)
    print(process)

# %% [markdown]
# The parameter `tau` is a property of the `OutgoingLongwave` subprocess:

# %%
ebm.subprocess['OutgoingLongwave'].tau

# %% [markdown]
# and the parameter `albedo` is a property of the `AbsorbedShortwave` subprocess:

# %%
ebm.subprocess['AbsorbedShortwave'].albedo

# %% [markdown]
# Let's make an exact clone of our model and then change these two parameters:

# %%
ebm2 = climlab.process_like(ebm)
print(ebm2)

# %%
ebm2.subprocess['OutgoingLongwave'].tau = 0.57
ebm2.subprocess['AbsorbedShortwave'].albedo = 0.32

# %% [markdown]
# Now our model is out of equilibrium and the climate will change!
#
# To see this without actually taking a step forward:

# %%
#  Computes diagnostics based on current state but does not change the state
ebm2.compute_diagnostics()
ebm2.ASR - ebm2.OLR

# %% [markdown]
# Shoud the model warm up or cool down?

# %% [markdown]
# Well, we can find out:

# %%
ebm2.Ts

# %%
ebm2.step_forward()

# %%
ebm2.Ts

# %% [markdown]
# ### Automatic timestepping

# %% [markdown]
# Often we want to integrate a model forward in time to equilibrium without needing to store information about the transient state.
#
# `climlab` offers convenience methods to do this easily:

# %%
ebm3 = climlab.process_like(ebm2)

# %%
ebm3.integrate_years(50)

# %%
#  What is the current temperature?
ebm3.Ts

# %%
#  How close are we to energy balance?
ebm3.ASR - ebm3.OLR

# %%
#  We should be able to accomplish the exact same thing with explicit timestepping
for n in range(608):
    ebm2.step_forward()

# %%
ebm2.Ts

# %%
ebm2.ASR - ebm2.OLR

# %% [markdown]
# ____________
# <a id='section5'></a>
#
# ## 5. Further `climlab` resources
# ____________

# %% [markdown]
# We will be using `climlab` extensively throughout this course. Lots of examples of more advanced usage are found here in the course notes. Here are some links to other resources:
#
# - The documentation is hosted at <https://climlab.readthedocs.io/en/latest/>
# - Source code (for both software and docs) are at <https://github.com/brian-rose/climlab>
# - [A video of a talk I gave about `climlab` at the 2018 AMS Python symposium](https://ams.confex.com/ams/98Annual/videogateway.cgi/id/44948?recordingid=44948) (January 2018)
# - [Slides from a talk and demonstration that I gave in Febrary 2018](https://livealbany-my.sharepoint.com/:f:/g/personal/brose_albany_edu/EuA2afxy5-hNkzNhHgkp_HYBYcJumR3l6ukRVIEl4W3MmA?e=sbXN0d) (The Apple Keynote version contains some animations that will not show up in the pdf version)

# %% [markdown] slideshow={"slide_type": "skip"}
# ____________
#
# ## Credits
#
# This notebook is part of [The Climate Laboratory](https://brian-rose.github.io/ClimateLaboratoryBook), an open-source textbook developed and maintained by [Brian E. J. Rose](http://www.atmos.albany.edu/facstaff/brose/index.html), University at Albany.
#
# It is licensed for free and open consumption under the
# [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/) license.
#
# Development of these notes and the [climlab software](https://github.com/brian-rose/climlab) is partially supported by the National Science Foundation under award AGS-1455071 to Brian Rose. Any opinions, findings, conclusions or recommendations expressed here are mine and do not necessarily reflect the views of the National Science Foundation.
# ____________

# %%
